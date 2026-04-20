import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR) # The root folder of the project

MODEL_PATH = os.path.join(PROJECT_ROOT, "fake_resume_model.pkl")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "tfidf_vectorizer.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "feature_scaler.pkl")

# API Config
API_TITLE = "AI Fake Resume Detector API"
API_VERSION = "1.0.0"
DEBUG = True
ALLOWED_HOSTS = ["*"]
