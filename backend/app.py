from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes import register_routes
from config import Config
from database import db
from models import User, Prediction

app = Flask(__name__)

# Load Configurations
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize Database
db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Register Routes
register_routes(app)

# Home Route
@app.route('/')
def home():
    return "SmartMed Backend Running"


# JWT Error Handlers

@jwt.unauthorized_loader
def missing_token(error):
    return {
        "error": "Authorization token required"
    }, 401


@jwt.invalid_token_loader
def invalid_token(error):
    return {
        "error": "Invalid token"
    }, 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return {
        "error": "Token expired"
    }, 401


with app.app_context():
    db.create_all()
    print("Database connected successfully!")
    print("Tables created successfully!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)