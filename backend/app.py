from flask import Flask
from routes import register_routes
from config import Config
from database import db
from models import User, Prediction

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

register_routes(app)

@app.route('/')
def home():
    return "SmartMed Backend Running"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database connected successfully!")

    app.run(debug=True)