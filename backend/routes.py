from flask import request, jsonify
from models import User, Prediction
from database import db
import bcrypt


def register_routes(app):

    # REGISTER API
    @app.route('/register', methods=['POST'])
    def register():

        data = request.get_json()

        name = data['name']
        email = data['email']
        password = data['password']

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "error": "Email already registered"
            }), 400

        # Hash password
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # Create user
        user = User(
            name=name,
            email=email,
            password=hashed.decode('utf-8')
        )

        # Save to database
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully"
        })


    # LOGIN API
    @app.route('/login', methods=['POST'])
    def login():

        data = request.get_json()

        email = data['email']
        password = data['password']

        # Find user
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # Check password
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):

            return jsonify({
                "message": "Login successful",
                "user_id": user.id
            })

        return jsonify({
            "error": "Invalid password"
        }), 401


    # PREDICT API
    @app.route('/predict', methods=['POST'])
    def predict():

        data = request.get_json()

        user_id = data['user_id']
        symptoms = data['symptoms']

        # Dummy prediction for now
        prediction = "Flu"
        confidence = "87%"

        # Save prediction
        new_prediction = Prediction(
            user_id=user_id,
            symptoms=",".join(symptoms),
            prediction=prediction,
            confidence=confidence
        )

        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            "prediction": prediction,
            "confidence": confidence
        })


    # HISTORY API
    @app.route('/history/<int:user_id>', methods=['GET'])
    def history(user_id):

        predictions = Prediction.query.filter_by(
            user_id=user_id
        ).all()

        result = []

        for p in predictions:
            result.append({
                "prediction": p.prediction,
                "symptoms": p.symptoms,
                "confidence": p.confidence
            })

        return jsonify(result)