import smtplib
from email.mime.text import MIMEText
import logging
from backend.config.config import settings

# Initialize logger for OTP email
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_otp_email(to_email: str, otp: str) -> bool:
    """
    Send an OTP code via email using a well-formatted HTML template.

    Args:
        to_email (str): Recipient's email address.
        otp (str): The OTP code to send.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Replace these with your actual SMTP server settings
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.SENDER_MAIL
    sender_password = settings.PASSKEY_MAIL
    
    subject = "Your One-Time Password (OTP)"
    
    # HTML message body for OTP email
    html = f"""\
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #2a7ae2;">One-Time Password (OTP) Verification</h2>
    <p>Dear User,</p>
    <p>Your OTP code is: <strong style="font-size: 1.3em;">{otp}</strong></p>
    <p>Please use this code to complete your verification. This OTP is valid for the next 10 minutes.</p>
    <br/>
    <p>Regards,<br/>Smart KYC</p>
  </body>
</html>
"""
    # Create MIMEText object with HTML subtype
    message = MIMEText(html, "html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        logger.info(f"OTP email sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as auth_err:
        logger.error(f"SMTP Authentication Error: {auth_err}")
        raise Exception(f"SMTP Authentication Error: {auth_err}")
    except smtplib.SMTPConnectError as conn_err:
        logger.error(f"SMTP Connection Error: {conn_err}")
        raise Exception(f"SMTP Connection Error: {conn_err}")
    except smtplib.SMTPException as smtp_err:
        logger.error(f"SMTP Error: {smtp_err}")
        raise Exception(f"SMTP Error: {smtp_err}")
    except Exception as e:
        logger.error(f"Error sending OTP email to {to_email}: {e}")
        raise Exception(f"An unexpected error occurred while sending OTP email: {e}")

