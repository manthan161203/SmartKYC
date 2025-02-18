import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.database.models.user_model import User
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from backend.config.config import Config

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, db) -> None:
    otp = generate_otp()
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.otp = otp
    user.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    db.commit()
    
    sender_email = Config.SENDER_MAIL
    receiver_email = email
    password = Config.PASSKEY_MAIL
    
    subject = "KYC System OTP Verification"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="background-color: #f4f4f4; padding: 20px; text-align: center; border-radius: 10px;">
            <h2 style="color: #007BFF;">KYC System OTP Verification</h2>
            <p style="font-size: 16px;">Hello,</p>
            <p style="font-size: 16px;">Thank you for using our KYC system. To complete your registration, please use the following One-Time Password (OTP):</p>
            
            <div style="background-color: #ffffff; padding: 20px; margin: 20px auto; border-radius: 5px; width: 60%; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <h3 style="font-size: 24px; color: #333; font-weight: bold;">Your OTP: <span style="color: #007BFF;">{otp}</span></h3>
                <p style="font-size: 16px; color: #555;">This OTP is valid for the next 5 minutes. Please enter it on the registration page to complete the process.</p>
            </div>

            <p style="font-size: 16px; color: #555;">If you did not request this OTP, please disregard this email or contact our support team for assistance.</p>

            <p style="font-size: 16px; color: #555;">Thank you for choosing our service.</p>
            <p style="font-size: 16px; font-weight: bold; color: #555;">Best regards,<br>The KYC System Team</p>

            <footer style="font-size: 12px; color: #888; margin-top: 20px;">
                <p>&copy; 2025 KYC System. All Rights Reserved.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def validate_otp(email: str, otp: str, db) -> bool:
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if datetime.now(timezone.utc) > user.otp_expiry.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    return True
