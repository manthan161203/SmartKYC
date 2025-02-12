from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from backend.database import SessionLocal
from backend.config import Config
from backend.database.models import User

app = Flask(__name__)

# Secret key for session management
app.config.from_object(Config)

@app.route('/register', methods=['POST'])
def register():
    db = SessionLocal()
    data = request.json
    
    # Hash the password before saving
    hashed_pw = generate_password_hash(data['password'])
    
    # Check if user already exists
    if db.query(User).filter(User.email == data['email']).first():
        db.close()
        return jsonify({"message": "User already exists!"}), 400
    
    # Create a new user
    user = User(username=data['username'], email=data['email'], phone=data['phone'], password=hashed_pw)
    db.add(user)
    db.commit()
    db.close()
    return jsonify({"message": "User registered successfully!"})