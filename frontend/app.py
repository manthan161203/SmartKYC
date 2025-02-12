from flask import Flask
from backend.config import Config
from backend.api.user_registration import app as registration_app
from backend.api.user_login import app as login_app

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register the routes from backend
app.register_blueprint(registration_app, url_prefix='/register')
app.register_blueprint(login_app, url_prefix='/login')

if __name__ == "__main__":
    app.run(debug=True)