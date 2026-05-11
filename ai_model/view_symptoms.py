import joblib

mlb = joblib.load("mlb_encoder.pkl")

print(list(mlb.classes_))