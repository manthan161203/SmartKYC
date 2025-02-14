import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.database.models import User
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, db) -> None:
    """Send OTP email using Gmail SMTP and save the OTP to the database."""
    otp = generate_otp()
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's OTP and expiration time
    user.otp = otp
    user.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    db.commit()
    
    # Send OTP via Gmail SMTP
    sender_email = "manthanlp3204@gmail.com"
    receiver_email = email
    password = "bewy jqdk rkef sonh"
    
    subject = "KYC System OTP Verification"
    body = f"Your OTP for KYC registration is: {otp}. It expires in 5 minutes."
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def validate_otp(email: str, otp: str, db) -> bool:
    """Validate OTP entered by the user."""
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if OTP exists and is valid
    if user.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Check if OTP has expired
    if datetime.now(timezone.utc) > user.otp_expiry.replace(tzinfo=timezone.utc):
    # Handle OTP expiration
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    # OTP is valid
    return True
