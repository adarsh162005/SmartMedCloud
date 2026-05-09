from flask import request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

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
        }), 201


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
                "error": "Invalid email or password"
            }), 401

        # Check password
        password_correct = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        )

        if not password_correct:
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        # Create JWT Token
        access_token = create_access_token(
            identity=str(user.id)
        )

        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }), 200


    # PREDICT API
    @app.route('/predict', methods=['POST'])
    @jwt_required()
    def predict():

        current_user_id = get_jwt_identity()

        data = request.get_json()

        symptoms = data['symptoms']

        if not symptoms:
            return jsonify({
                "error": "Symptoms are required"
            }), 400

        # Dummy prediction for now
        prediction = "Flu"
        confidence = "87%"

        # Save prediction
        new_prediction = Prediction(
            user_id=current_user_id,
            symptoms=",".join(symptoms),
            prediction=prediction,
            confidence=confidence
        )

        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            "prediction": prediction,
            "confidence": confidence
        }), 200


    # HISTORY API
    @app.route('/history', methods=['GET'])
    @jwt_required()
    def history():

        current_user_id = get_jwt_identity()

        predictions = Prediction.query.filter_by(
            user_id=current_user_id
        ).all()

        result = []

        for p in predictions:

            result.append({
                "prediction": p.prediction,
                "symptoms": p.symptoms,
                "confidence": p.confidence,
                "created_at": p.created_at
            })

        return jsonify(result), 200