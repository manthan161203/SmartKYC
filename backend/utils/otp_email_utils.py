import smtplib
from email.mime.text import MIMEText
import logging
from backend.config.config import settings

# Initialize logger for email sending
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_email(to_email: str, full_name: str, email_type: str, otp: str = None, reset_link: str = None) -> bool:
    """
    Send an email for OTP or password reset using a well-formatted HTML template.

    Args:
        to_email (str): Recipient's email address.
        full_name (str): The full name of the recipient.
        email_type (str): Type of email to send ("otp" or "reset_password").
        otp (str, optional): The OTP code (only required for OTP emails).
        reset_link (str, optional): The password reset link (only required for password reset emails).

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # SMTP settings
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.SENDER_MAIL
    sender_password = settings.PASSKEY_MAIL

    print(f"SMTP Server: {reset_link}")
    
    if email_type == "otp":
        subject = "Your One-Time Password (OTP) - Smart KYC"
        html = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f7fc; margin: 0; padding: 0;">
            <table role="presentation" style="width: 100%; max-width: 600px; margin: 20px auto; border: 1px solid #ddd; border-radius: 8px; background-color: #ffffff;">
                <tr>
                    <td style="background-color: #2a7ae2; color: white; text-align: center; padding: 15px 0; font-size: 24px; font-weight: bold; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                        One Time Password (OTP)
                    </td>
                </tr>
                <tr>
                    <td style="padding: 30px; text-align: center;">
                        <p style="font-size: 18px; color: #333333; line-height: 1.5;">
                            Hello {full_name},<br><br>
                            Your One-Time Password (OTP) is:<br><br>
                            <strong style="font-size: 30px; color: #2a7ae2;">{otp}</strong><br><br>
                            Please use this OTP to complete your verification.<br>
                            <span style="font-size: 14px; color: #888;">This OTP will expire in 10 minutes.</span>
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #f4f7fc; color: #333333; text-align: center; padding: 15px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                        <p style="font-size: 12px;">If you did not request this OTP, please ignore this email.</p>
                        <p style="font-size: 12px;">Regards,<br><strong>Smart KYC Team</strong></p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    elif email_type == "reset_password":
        subject = "Password Reset Request - Smart KYC"
        html = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f7fc; margin: 0; padding: 0;">
            <table role="presentation" style="width: 100%; max-width: 600px; margin: 20px auto; border: 1px solid #ddd; border-radius: 8px; background-color: #ffffff;">
                <tr>
                    <td style="background-color: #e22a2a; color: white; text-align: center; padding: 15px 0; font-size: 24px; font-weight: bold; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                        Password Reset Request
                    </td>
                </tr>
                <tr>
                    <td style="padding: 30px; text-align: center;">
                        <p style="font-size: 18px; color: #333333; line-height: 1.5;">
                            Hello {full_name},<br><br>
                            We received a request to reset your password. Click the link below to set a new password:<br><br>
                            <a href="{reset_link}" style="display: inline-block; background-color: #e22a2a; color: white; padding: 12px 20px; text-decoration: none; font-size: 16px; border-radius: 5px;">Reset Password</a><br><br>
                            If you didn't request this, please ignore this email.<br>
                            <span style="font-size: 14px; color: #888;">This link will expire in 30 minutes.</span>
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #f4f7fc; color: #333333; text-align: center; padding: 15px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                        <p style="font-size: 12px;">Regards,<br><strong>Smart KYC Team</strong></p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    else:
        raise ValueError("Invalid email type. Must be 'otp' or 'reset_password'.")

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

        logger.info(f"Email sent successfully to {to_email}")
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
        logger.error(f"Error sending email to {to_email}: {e}")
        raise Exception(f"An unexpected error occurred while sending email: {e}")