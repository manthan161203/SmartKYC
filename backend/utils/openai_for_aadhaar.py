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

def build_prompt(ocr_json_str):
    """
    Build a prompt using the OCR JSON output.
    The OCR JSON is expected to have keys: 'tesseract', 'easyocr', 'paddleocr'.
    The prompt instructs OpenAI to extract the following five fields:
      - aadhaar: three groups of four digits (no spaces)
      - dob: the earliest date (dd/mm/yyyy format)
      - gender: e.g., "MALE" or "FEMALE"
      - name: the person's name
      - address: if available; otherwise null
    Return the prompt as a string.
    """
    # Convert JSON string to dictionary
    ocr_data = json.loads(ocr_json_str)
    combined_text = " ".join(ocr_data.get(k, "") for k in ["tesseract", "easyocr", "paddleocr"])
    prompt = (
        "Extract the following fields from the OCR output below. "
        "For 'dob', choose the earliest date (dd/mm/yyyy format). "
        "If a field is missing, return null. "
        "Return the result as JSON string with keys: 'aadhaar', 'dob', 'gender', 'name', 'address'.\n\n"
        "OCR Output:\n" + combined_text
    )
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


# You can call process_image("your_image_path") elsewhere and then use build_prompt and query_openai.
# For example:
#
# ocr_json = process_image("front.jpg")
# prompt = build_prompt(ocr_json)
# extracted_response = query_openai(prompt)
# cleaned_response = remove_markdown(extracted_response)

# print(cleaned_response)
# Then export 'cleaned_response' as needed.
