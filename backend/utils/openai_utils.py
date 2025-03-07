import json
import logging
import re
from openai import OpenAI
from backend.config.config import settings
from backend.utils.image_processing_ocr import process_image

# Initialize OpenAI client using your settings
client = OpenAI(api_key=settings.OPENAI_KEY)

logging.basicConfig(
    filename="processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def build_prompt(ocr_json_str, side="front_aadhaar"):
    """
    Build a prompt using the OCR JSON output.
    The OCR JSON is expected to have keys: 'tesseract', 'easyocr', 'paddleocr'.
    
    Options for side:
    - "front_aadhaar": Extract aadhaar, dob, gender, and name.
    - "back_aadhaar": Extract the full address as one string.
    - "pan_card": Extract pan, name, father_name, and dob.
    
    If a field is missing, return null.
    Return the result as a JSON string.
    """
    ocr_data = json.loads(ocr_json_str)
    combined_text = " ".join(ocr_data.get(k, "") for k in ["tesseract", "easyocr", "paddleocr"])
    
    if side.lower() == "front_aadhaar":
        prompt = (
            "Extract the following fields from the OCR output:\n"
            "- aadhaar: three groups of 4 digits\n"
            "- dob: earliest date in dd/mm/yyyy\n"
            "- gender: 'MALE' or 'FEMALE'\n"
            "- name: full name only character\n"
            "If missing, use null. Return as JSON with keys: 'aadhaar', 'dob', 'gender', 'name'.\n\n"
            "OCR Output:\n" + combined_text
        )
    elif side.lower() == "back_aadhaar":
        prompt = (
            "Extract the full address as a single string from the OCR output below. "
            "The address is located after 'Address:' on the back of an Aadhaar card. "
            "Remove any OCR noise and meaningless words (such as garbled or spurious text) that do not contribute to a proper address. "
            "Ensure that any Indian names or terms are correctly formatted. "
            "Return the cleaned address as JSON with the key 'address'.\n\n"
            "OCR Output:\n" + combined_text
        )

    elif side.lower() == "pan_card":
        prompt = (
            "Extract the following fields from the OCR output below:\n"
            "- pan: a 10-character alphanumeric code (e.g., GQSPP8532A)\n"
            "- name: full name\n"
            "- father_name: father's full name\n"
            "- dob: date of birth in dd/mm/yyyy format\n"
            "If missing, return null. Return as JSON with keys: 'pan', 'name', 'father_name', 'dob'.\n\n"
            "OCR Output:\n" + combined_text
        )
    else:
        prompt = "Invalid side parameter."
    return prompt

def query_openai(prompt):
    """
    Query OpenAI's Chat API using the given prompt and return the response text.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error("Error querying OpenAI: %s", e)
        raise

def remove_markdown(json_text):
    """
    Remove markdown formatting (i.e., triple backticks and optional "json" label)
    from the given text.
    """
    text = re.sub(r'^```(?:json)?\s*', '', json_text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    return text

# Example usage:
# ocr_json = process_image("/backend/images/front_manthan_aadhaar.jpg")
# prompt_front = build_prompt(ocr_json, side="front_aadhaar")
# front_response = query_openai(prompt_front)
# cleaned_front = remove_markdown(front_response)
# print("Front Aadhaar Data:", cleaned_front)

# ocr_json_back = process_image("/backend/images/back_manthan_aadhaar.jpg")
# prompt_back = build_prompt(ocr_json_back, side="back_aadhaar")
# back_response = query_openai(prompt_back)
# cleaned_back = remove_markdown(back_response)
# print("Back Aadhaar Address:", cleaned_back)

# ocr_json_pan = process_image("/backend/images/pan_card.jpg")
# prompt_pan = build_prompt(ocr_json_pan, side="pan_card")
# pan_response = query_openai(prompt_pan)
# cleaned_pan = remove_markdown(pan_response)
# print("PAN Card Data:", cleaned_pan)
