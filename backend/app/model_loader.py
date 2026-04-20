import joblib
import os
from app.config import MODEL_PATH, VECTORIZER_PATH, SCALER_PATH

class ModelLoader:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and os.path.exists(SCALER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            print("Model, Vectorizer, and Scaler loaded successfully.")
        else:
            print(f"Error: Required artifacts not found at {MODEL_PATH}, {VECTORIZER_PATH}, or {SCALER_PATH}")

model_loader = ModelLoader()
