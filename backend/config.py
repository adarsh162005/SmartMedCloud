from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Admin123@localhost:5432/smartmed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "smartmedcloudjwtsecretkey2026"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)