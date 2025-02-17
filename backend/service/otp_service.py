import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.database.models import User
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
    body = f"Your OTP for KYC registration is: {otp}."
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
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
