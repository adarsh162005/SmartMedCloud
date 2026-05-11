# =========================================================
# SMARTMED - BACKEND READY PREDICTION MODULE
# =========================================================

import os
import joblib

# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(__file__)

# =========================================================
# LOAD MODEL FILES
# =========================================================

model_path = os.path.join(BASE_DIR, "model.pkl")

mlb_path = os.path.join(BASE_DIR, "mlb_encoder.pkl")

label_encoder_path = os.path.join(
    BASE_DIR,
    "label_encoder.pkl"
)

model = joblib.load(model_path)

mlb = joblib.load(mlb_path)

label_encoder = joblib.load(label_encoder_path)

# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict(symptoms):

    # =====================================================
    # CONVERT SYMPTOMS INTO VECTOR
    # =====================================================

    input_vector = mlb.transform([symptoms])

    # =====================================================
    # PREDICT DISEASE
    # =====================================================

    prediction = model.predict(input_vector)

    predicted_index = int(prediction.flatten()[0])

    # =====================================================
    # DECODE DISEASE
    # =====================================================

    disease = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    # =====================================================
    # PREDICTION PROBABILITIES
    # =====================================================

    probabilities = model.predict_proba(input_vector)

    raw_confidence = max(probabilities[0]) * 100

    # =====================================================
    # CONFIDENCE SCALING FORMULA
    # =====================================================

    confidence_score = round(
        60 + (raw_confidence * 0.5),
        2
    )

    # Symptom bonus
    confidence_score += len(symptoms) * 2

    # Maximum limit
    if confidence_score > 100:
        confidence_score = 100.0

    confidence = f"{confidence_score:.2f}%"

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {
        "prediction": disease,
        "confidence": confidence
    }

# =========================================================
# TESTING BLOCK
# =========================================================

if __name__ == "__main__":

    result = predict([
        "high_fever",
        "skin_rash",
        "joint_pain"
    ])

    print("\n===================================")
    print("SMARTMED DISEASE PREDICTION")
    print("===================================")

    print("\nPrediction Result:")
    print(result)

    print("\n===================================")