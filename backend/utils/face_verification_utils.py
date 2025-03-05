import cv2
import json
import matplotlib.pyplot as plt
from deepface import DeepFace
from typing import List, Dict, Union, Optional
import math

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    """
    Converts a face distance into a confidence score in [0,1].
    When the face distance is less than or equal to the threshold,
    the confidence is higher (closer to 1). For distances above the threshold,
    confidence decreases.
    
    This function is one possible heuristic; it is non-linear,
    to reflect that small differences in distance when faces are very similar
    might mean a large change in perceived similarity.
    """
    if face_distance > face_match_threshold:
        # For distances above the threshold, a simple linear scale is used.
        range_ = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range_ * 2.0)
        return linear_val
    else:
        # For distances below the threshold, we adjust the confidence non-linearly.
        range_ = face_match_threshold
        linear_val = 1.0 - (face_distance / (range_ * 2.0))
        # This additional term boosts confidence for very close distances.
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


def detect_faces(img_path: str, db_path: str = "backend/images") -> Optional[List[Dict]]:
    """
    Detects faces in an image and draws bounding boxes around them.

    Args:
        img_path (str): Path to the input image.
        db_path (str): Path to the database of images.

    Returns:
        List[Dict]: List of detected faces with coordinates or None if no faces are detected.
    """
    try:
        detected_faces = DeepFace.find(img_path=img_path, db_path=db_path, enforce_detection=False)
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if isinstance(detected_faces, list) and len(detected_faces) > 0:
            df = detected_faces[0]
            faces = []
            for _, row in df.iterrows():
                x, y, w, h = int(row["source_x"]), int(row["source_y"]), int(row["source_w"]), int(row["source_h"])
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                faces.append({"x": x, "y": y, "w": w, "h": h})

            plt.imshow(image)
            plt.axis("off")
            plt.show()

            return faces

    except ValueError as e:
        print(f"Error: {e}")
    
    return None


def analyze_face(img_path: str) -> Optional[Dict]:
    """
    Analyzes the given image for age, gender, race, and emotion.

    Args:
        img_path (str): Path to the input image.

    Returns:
        Dict: Analysis result with age, gender, race, and emotion or None if an error occurs.
    """
    try:
        demography = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race', 'emotion'])
        print(json.dumps(demography, indent=4))
        return demography

    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def verify_faces(img1_path: str, img2_path: str, model_name: str = 'ArcFace') -> Optional[Dict]:
    """
    Verifies if two images belong to the same person using face verification.

    Args:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.
        model_name (str): Face recognition model (default: ArcFace).

    Returns:
        Dict: Verification result containing 'verified', 'distance', and 'threshold' or None if an error occurs.
    """
    try:
        verification_obj = DeepFace.verify(
            img1_path, img2_path, model_name=model_name, detector_backend='retinaface', distance_metric='cosine'
        )

        faces1 = DeepFace.extract_faces(img_path=img1_path, detector_backend='retinaface', enforce_detection=False)
        faces2 = DeepFace.extract_faces(img_path=img2_path, detector_backend='retinaface', enforce_detection=False)

        def draw_face_boxes(image: cv2.typing.MatLike, faces: List[Dict[str, Union[int, Dict]]]) -> cv2.typing.MatLike:
            for face in faces:
                facial_area = face["facial_area"]
                x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return image

        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        img1_with_boxes = draw_face_boxes(img1_rgb.copy(), faces1)
        img2_with_boxes = draw_face_boxes(img2_rgb.copy(), faces2)
        
        # Calculate match percentage using the distance metric
        distance = verification_obj['distance']
        threshold = verification_obj['threshold']

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(img1_with_boxes)
        plt.axis("off")
        plt.title("Image 1 with Face Box")

        plt.subplot(1, 2, 2)
        plt.imshow(img2_with_boxes)
        plt.axis("off")
        plt.title("Image 2 with Face Box")
        
        confidence = face_distance_to_conf(distance, face_match_threshold=threshold)
        match_percentage = confidence * 100
        
        plt.suptitle(
            f"Face Verified: {verification_obj['verified']}\n"
            f"Distance Metric: {verification_obj.get('distance_metric', 'cosine')}\n"
            f"Match Percentage: {match_percentage:.2f}%\n",
            fontsize=16,
            color='red'
        )
        plt.show()

        result = {
            "verified": verification_obj["verified"],
            "distance_metric": verification_obj.get('distance_metric', 'cosine'),
            "distance": verification_obj['distance'],
            "threshold": verification_obj['threshold'],
            "percentage": f"{match_percentage:.2f}"
        }

        return result

    except Exception as e:
        print(f"An error occurred: {e}")

    return None