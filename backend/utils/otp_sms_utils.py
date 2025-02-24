import requests
import logging

# Initialize logger for OTP SMS
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_otp_sms(phone_number: str, otp: str) -> bool:
    """
    Send an OTP code via SMS using a formatted message.

    Args:
        phone_number (str): Recipient's phone number.
        otp (str): The OTP code to send.

    Returns:
        bool: True if the SMS was sent successfully, False otherwise.
    """
    # Replace with your SMS provider's API URL and credentials
    api_url = "https://api.smsprovider.com/send"
    api_key = "your_sms_provider_api_key"
    sender_id = "your_sender_id"
    
    # Format the OTP message for SMS
    message = f"Your OTP code is {otp}. Use it to complete your verification. Valid for 10 minutes."
    
    payload = {
        'api_key': api_key,
        'to': phone_number,
        'from': sender_id,
        'message': message,
    }

    try:
        response = requests.post(api_url, data=payload)
        response_data = response.json()
        
        if response_data.get("status") == "success":
            logger.info(f"OTP SMS sent successfully to {phone_number}")
            return True
        else:
            logger.error(f"Failed to send OTP SMS to {phone_number}: {response_data.get('message')}")
            return False
    except Exception as e:
        logger.error(f"Error sending OTP SMS to {phone_number}: {e}")
        return False
