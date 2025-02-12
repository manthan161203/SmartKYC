from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from backend.database import SessionLocal
from backend.database.models import User
from backend.config import Config

app = Flask(__name__)

# Secret key for session management
app.config.from_object(Config)

@app.route('/login', methods=['POST'])
def login():
    db = SessionLocal()
    data = request.json
    
    # Check if user exists by email
    user = db.query(User).filter(User.email == data['email']).first()
    if not user:
        db.close()
        return jsonify({"message": "User not found!"}), 404
    
    # Check if the password matches
    if not check_password_hash(user.password, data['password']):
        db.close()
        return jsonify({"message": "Incorrect password!"}), 400
    
    db.close()
    return jsonify({"message": "Login successful!"})