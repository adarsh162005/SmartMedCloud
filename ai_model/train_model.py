# =========================================================
# SMARTMED - PROFESSIONAL CATBOOST TRAINING
# =========================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import (
    LabelEncoder,
    MultiLabelBinarizer
)

from sklearn.metrics import accuracy_score

from catboost import CatBoostClassifier

# =========================================================
# LOAD DATASET
# =========================================================

dataset_df = pd.read_csv("ai_model/dataset.csv")

# =========================================================
# HANDLE MISSING VALUES
# =========================================================

dataset_df.fillna("", inplace=True)

# =========================================================
# CLEAN TEXT
# =========================================================

dataset_df = dataset_df.map(
    lambda x: x.strip().lower()
    if isinstance(x, str)
    else x
)

# =========================================================
# EXTRACT SYMPTOM COLUMNS
# =========================================================

symptom_columns = [
    col for col in dataset_df.columns
    if "symptom" in col.lower()
]

# =========================================================
# IMPORTANT:
# KEEP DUPLICATES
# =========================================================

print("\nUsing FULL dataset for training")

print("Dataset Shape:", dataset_df.shape)

# =========================================================
# CREATE SYMPTOM LIST
# =========================================================

symptom_data = []

for _, row in dataset_df.iterrows():

    symptoms = []

    for col in symptom_columns:

        symptom = row[col]

        if symptom != "":
            symptoms.append(symptom)

    symptom_data.append(symptoms)

# =========================================================
# MULTI LABEL BINARIZER
# =========================================================

mlb = MultiLabelBinarizer()

X = mlb.fit_transform(symptom_data)

# =========================================================
# LABEL ENCODER
# =========================================================

le = LabelEncoder()

y = le.fit_transform(
    dataset_df["Disease"]
)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# =========================================================
# PROFESSIONAL CATBOOST MODEL
# =========================================================

model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.03,
    depth=8,
    loss_function='MultiClass',
    eval_metric='Accuracy',
    verbose=100
)

# =========================================================
# TRAIN MODEL
# =========================================================

print("\nTraining Model...\n")

model.fit(
    X_train,
    y_train
)

# =========================================================
# TEST MODEL
# =========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# =========================================================
# SAVE MODEL FILES
# =========================================================

joblib.dump(model, "model.pkl")

joblib.dump(mlb, "mlb_encoder.pkl")

joblib.dump(le, "label_encoder.pkl")

print("\nModel Saved Successfully")