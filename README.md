# SmartMed Cloud

AI-Powered Disease Prediction Platform using Flask, PostgreSQL, and Machine Learning.

---

# Overview

SmartMed Cloud is a full-stack healthcare web application that predicts diseases based on user-selected symptoms using a trained Machine Learning model.

The system provides:

* Secure JWT-based authentication
* AI-powered disease prediction
* Prediction history tracking
* PostgreSQL database integration
* Responsive frontend dashboard
* REST API backend using Flask

The project combines Artificial Intelligence, Cloud Computing, Backend Development, Database Management, and Frontend Integration into a complete healthcare platform.

---

# Features

* User Registration and Login
* JWT Authentication
* AI Disease Prediction
* Prediction Confidence Scores
* PostgreSQL Database Storage
* Prediction History Tracking
* Responsive Dashboard UI
* REST API Architecture
* Flask Backend Integration
* Machine Learning Model Integration

---

# Tech Stack

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Flask
* Flask-JWT-Extended
* Flask-SQLAlchemy
* Flask-CORS

## Database

* PostgreSQL

## Machine Learning

* CatBoost
* Scikit-learn
* MultiLabelBinarizer
* LabelEncoder

---

# Project Structure

```bash
SmartMedCloud/
│
├── ai_model/
│   ├── catboost_info/
│   ├── predict.py
│   ├── train_model.py
│   ├── view_symptoms.py
│   ├── model.pkl
│   ├── mlb_encoder.pkl
│   ├── label_encoder.pkl
│   └── dataset.csv
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── history.html
│   ├── script.js
│   └── style.css
│
├── README.md
└── LICENSE
```

---

## Live Demo

Frontend: https://smart-med-cloud.vercel.app

Backend API: https://smartmed-backend-h7qx.onrender.com

---

# API Endpoints

## Register User

```http
POST /register
```

### Request Body

```json
{
  "name": "Adarsh",
  "email": "adarsh@gmail.com",
  "password": "password123"
}
```

---

## Login User

```http
POST /login
```

### Response

```json
{
  "token": "jwt_token",
  "user": {
    "id": 1,
    "name": "Adarsh",
    "email": "adarsh@gmail.com"
  }
}
```

---

## Predict Disease

```http
POST /predict
```

### Headers

```http
Authorization: Bearer <jwt_token>
```

### Request Body

```json
{
  "symptoms": [
    "high_fever",
    "joint_pain",
    "vomiting"
  ]
}
```

### Response

```json
{
  "prediction": "malaria",
  "confidence": "73.46%"
}
```

---

## Prediction History

```http
GET /history
```

### Headers

```http
Authorization: Bearer <jwt_token>
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/adarsh162005/SmartMedCloud.git
```

---

## 2. Navigate to Backend

```bash
cd SmartMedCloud/backend
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Configure PostgreSQL

Create PostgreSQL database:

```text
smartmed
```

Update `config.py`:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/smartmed"
```

---

## 7. Run Backend

```bash
python app.py
```

---

## 8. Run Frontend

Open frontend files using VS Code Live Server.

---

# Machine Learning Model

The disease prediction system uses a trained CatBoost classification model.

### Model Pipeline

* Symptom preprocessing using MultiLabelBinarizer
* Disease label encoding using LabelEncoder
* Disease prediction using CatBoost Classifier
* Confidence score generation

---

# Database Tables

## users

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| name     | String  |
| email    | String  |
| password | String  |

---

## predictions

| Column     | Type      |
| ---------- | --------- |
| id         | Integer   |
| user_id    | Integer   |
| symptoms   | Text      |
| prediction | String    |
| confidence | String    |
| created_at | Timestamp |

---

# Future Improvements

* Cloud Deployment
* Doctor Recommendation System
* PDF Medical Reports
* Email Notifications
* Symptom Search Bar
* Data Visualization Dashboard
* Mobile App Integration

---

# License

This project is licensed under the MIT License.

---

# Authors

* Adarsh V Kapse
* Team SmartMed Cloud
