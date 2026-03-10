import json
import logging
import re
import requests
from backend.config.config import settings
from backend.utils.image_processing_ocr import process_image

logging.basicConfig(
    filename="processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def build_prompt(ocr_json_str, side="front_aadhaar"):
    """
    Build a prompt using the OCR JSON output. The OCR JSON is expected to have keys:
    'tesseract', 'easyocr', 'paddleocr'. The values are concatenated together to form the combined OCR text.
    
    Options for side:
    - "front_aadhaar": Extract aadhaar, dob, gender, and name.
    - "back_aadhaar": Extract the full address.
    - "pan_card": Extract pan, name, father_name, and dob.
    
    If a field is missing, return null.
    Return the prompt string.
    """
    ocr_data = json.loads(ocr_json_str)
    combined_text = " ".join(ocr_data.get(k, "") for k in ["easyocr"])
    
    if side.lower() == "aadhaar_front":
        prompt = (
            "You are provided with OCR text extracted from the front side of an Aadhaar card. "
            "Extract the following fields and return ONLY a JSON object (with no extra text):\n\n"
            "  - \"aadhaar\": A valid Aadhaar number, formatted as three groups of 4 digits (e.g., \"1234 5678 9012\").\n"
            "  - \"dob\": The earliest date found in the format dd/mm/yyyy. If multiple dates exist, select the earliest.\n"
            "  - \"gender\": Either \"MALE\" or \"FEMALE\" (case-insensitive).\n"
            "  - \"name\": The full name (only alphabetic characters and spaces).\n\n"
            "If any field is missing, its value should be null.\n\n"
            "OCR Output:\n" + combined_text
        )
    elif side.lower() == "aadhaar_back":
        prompt = (
            "You are provided with OCR text extracted from the back side of an Aadhaar card. "
            "Extract the full address as a single string. The address is located after the label 'Address:'. "
            "Clean the text by removing any noise, garbled words, or extraneous characters. "
            "Return ONLY a JSON object with a single key \"address\". If no valid address is found, set its value to null.\n\n"
            "OCR Output:\n" + combined_text
        )
    elif side.lower() == "pan":
        prompt = (
            "You are provided with OCR text extracted from a PAN card. "
            "Extract the following fields and return ONLY a JSON object (with no extra text):\n\n"
            "  - \"pan\": A valid PAN number (exactly 10 alphanumeric characters, e.g., \"ABCDE1234F\").\n"
            "  - \"name\": The full name as printed on the PAN card.\n"
            "  - \"father_name\": The full name of the father as printed on the PAN card.\n"
            "  - \"dob\": The date of birth in dd/mm/yyyy format.\n\n"
            "If any field is missing, set its value to null.\n\n"
            "OCR Output:\n" + combined_text
        )
    else:
        prompt = "Invalid side parameter."
    return prompt

def query_openai(prompt):
    """
    Query Gemini API using the given prompt and return the response text.
    """
    try:
        if not settings.GEMINI_KEY:
            raise ValueError("GEMINI_KEY is not configured. Set it in .env to enable document extraction.")

        model = "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 250
            }
        }
        response = requests.post(
            url,
            params={"key": settings.GEMINI_KEY},
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )
        if not text:
            raise ValueError(f"Unexpected Gemini response: {data}")
        return text
    except Exception as e:
        logging.error("Error querying Gemini: %s", e)
        raise

def remove_markdown(json_text):
    """
    Remove markdown formatting (triple backticks and optional "json" label)
    from the given text.
    """
    text = re.sub(r'^```(?:json)?\s*', '', json_text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    return text

# Example usage:
# Process image to get OCR JSON output (assumed to contain keys "tesseract", "easyocr", "paddleocr")
# ocr_json_front = process_image("/backend/images/front_manthan_aadhaar.jpg")
# prompt_front = build_prompt(ocr_json_front, side="front_aadhaar")
# front_response = query_openai(prompt_front)
# cleaned_front = remove_markdown(front_response)
# print("Front Aadhaar Data:", cleaned_front)
#
# ocr_json_back = process_image("/backend/images/back_manthan_aadhaar.jpg")
# prompt_back = build_prompt(ocr_json_back, side="back_aadhaar")
# back_response = query_openai(prompt_back)
# cleaned_back = remove_markdown(back_response)
# print("Back Aadhaar Address:", cleaned_back)
#
# ocr_json_pan = process_image("/backend/images/pan_card.jpg")
# prompt_pan = build_prompt(ocr_json_pan, side="pan_card")
# pan_response = query_openai(prompt_pan)
# cleaned_pan = remove_markdown(pan_response)
# print("PAN Card Data:", cleaned_pan)
