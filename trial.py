# from backend.utils.face_verification_utils import detect_faces, analyze_face, verify_faces

# print(detect_faces("backend/images/front.jpg"))
# print(analyze_face("backend/images/front.jpg"))







from backend.utils.image_processing_ocr import process_image
from backend.utils.openai_utils import build_prompt, query_openai, remove_markdown

# Example usage:
ocr_json = process_image("https://nwgdoijoeaatwyodhoty.supabase.co/storage/v1/object/sign/documents/uploads/47/aadhaar_front/bcb8f409-8eb1-4557-867a-91bcd450ead9_front_manthan_aadhaar.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJkb2N1bWVudHMvdXBsb2Fkcy80Ny9hYWRoYWFyX2Zyb250L2JjYjhmNDA5LThlYjEtNDU1Ny04NjdhLTkxYmNkNDUwZWFkOV9mcm9udF9tYW50aGFuX2FhZGhhYXIuanBnIiwiaWF0IjoxNzQxNTg1NjM2LCJleHAiOjE3NDQxNzc2MzZ9.YUhf_a5U50NGu4flKDp95fRmf4M04N3lYghM39UYC4Q")
prompt_front = build_prompt(ocr_json, side="front_aadhaar")
front_response = query_openai(prompt_front)
cleaned_front = remove_markdown(front_response)
print(ocr_json)
print("Front Aadhaar Data:", cleaned_front)

# ocr_json_back = process_image("backend/images/back_lalit_aadhaar.jpg")
# prompt_back = build_prompt(ocr_json_back, side="back_aadhaar")
# back_response = query_openai(prompt_back)
# cleaned_back = remove_markdown(back_response)
# print("Back Aadhaar Address:", cleaned_back)

# ocr_json_pan = process_image("backend/images/front_lalit_pan.jpg")
# prompt_pan = build_prompt(ocr_json_pan, side="pan_card")
# pan_response = query_openai(prompt_pan)
# cleaned_pan = remove_markdown(pan_response)
# print("PAN Card Data:", cleaned_pan)


# from supabase import create_client
# from backend.config.config import settings

# supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
# response = supabase.storage.get_bucket("documents")

# print(response)