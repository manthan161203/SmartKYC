import os

import requests
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU (Force CPU-only execution)
import cv2
import numpy as np
import re
import json
import logging
import easyocr
from paddleocr import PaddleOCR

logging.basicConfig(
    filename="processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_image(image_url):
    """Download the image from the given URL and return it as a numpy array."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for failed requests
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)  # Decode image
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image: {e}")
        raise


# ---------- Utility Function ----------

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# ---------- Image Processing Functions ----------

def invert_image(img):
    try:
        return cv2.bitwise_not(img)
    except Exception as e:
        logging.error("Error in invert_image: %s", e)
        raise

def rescale_image(img, scale_percent=60):
    try:
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    except Exception as e:
        logging.error("Error in rescale_image: %s", e)
        raise

def grayscale(image):
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logging.error("Error in grayscale: %s", e)
        raise

def binarize_image(img):
    try:
        gray_image = grayscale(img)
        # Use adaptive thresholding for varying lighting conditions
        im_bw = cv2.adaptiveThreshold(gray_image, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY,
                                      blockSize=11,
                                      C=2)
        return im_bw
    except Exception as e:
        logging.error("Error in binarize_image: %s", e)
        raise

def noise_removal(image):
    try:
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return image
    except Exception as e:
        logging.error("Error in noise_removal: %s", e)
        raise

def thin_font(image):
    try:
        image = cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        return cv2.bitwise_not(image)
    except Exception as e:
        logging.error("Error in thin_font: %s", e)
        raise

def thick_font(image):
    try:
        image = cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        return cv2.bitwise_not(image)
    except Exception as e:
        logging.error("Error in thick_font: %s", e)
        raise

# ---------- Rotation / Deskewing Functions ----------

def getSkewAngle(cvImage) -> float:
    try:
        newImage = cvImage.copy()
        if len(newImage.shape) == 3:
            gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        else:
            gray = newImage
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=5)
        contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("No contours found for deskewing.")
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
        return -1.0 * angle
    except Exception as e:
        logging.error("Error in getSkewAngle: %s", e)
        raise

def rotateImage(cvImage, angle: float):
    try:
        newImage = cv2.copyMakeBorder(cvImage, 0, 0, 0, 0, cv2.BORDER_REPLICATE)
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except Exception as e:
        logging.error("Error in rotateImage: %s", e)
        raise

def deskew(cvImage):
    try:
        angle = getSkewAngle(cvImage)
        return rotateImage(cvImage, -1.0 * angle)
    except Exception as e:
        logging.error("Error in deskew: %s", e)
        raise

# ---------- Border Functions ----------

def remove_borders(image):
    try:
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
            cnt = cntsSorted[-1]
            x, y, w, h = cv2.boundingRect(cnt)
            return image[y:y+h, x:x+w]
        else:
            logging.warning("No contours found for border removal; returning original image.")
            return image
    except Exception as e:
        logging.error("Error in remove_borders: %s", e)
        raise

def add_border(image, border_size=150, color=[255, 255, 255]):
    try:
        top = bottom = left = right = border_size
        return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    except Exception as e:
        logging.error("Error in add_border: %s", e)
        raise

# ---------- OCR Functions ----------

def ocr_easyocr_image(img):
    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(img, detail=0, text_threshold=0.7,
                                low_text=0.3, link_threshold=0.5)
        text = " ".join(result)
        return clean_text(text)
    except Exception as e:
        logging.error("Error in ocr_easyocr_image: %s", e)
        raise

def ocr_paddleocr_image(img):
    try:
        ocr_model = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)
        result = ocr_model.ocr(img, cls=True)
        text = " ".join([line[1][0] for page in result for line in page])
        return clean_text(text)
    except Exception as e:
        logging.error("Error in ocr_paddleocr_image: %s", e)
        raise

# ---------- Main Processing Function ----------
def process_image(image_url):
    """Download and process the image for OCR."""
    try:
        img = download_image(image_url)
        if img is None:
            raise FileNotFoundError(f"Failed to download image from {image_url}")
        logging.info("Successfully downloaded image: %s", image_url)
    except Exception as e:
        logging.error("Error loading image: %s", e)
        raise

    try:
        # Apply pre-processing techniques
        im_bw = binarize_image(img)
        no_noise = noise_removal(im_bw)
        fixed = deskew(no_noise)  # noqa: F841

        # Choose the final image for OCR
        final_img = no_noise
        logging.info("Image processing completed.")
    except Exception as e:
        logging.error("Error during image processing: %s", e)
        raise

    try:
        easyocr_text = ocr_easyocr_image(final_img)
        paddleocr_text = ocr_paddleocr_image(final_img)
        logging.info("OCR processing completed.")
    except Exception as e:
        logging.error("Error during OCR processing: %s", e)
        raise

    result = {
        "easyocr": easyocr_text,
        "paddleocr": paddleocr_text
    }

    return json.dumps(result, indent=4)