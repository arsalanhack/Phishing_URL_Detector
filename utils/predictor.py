import os
import joblib
import numpy as np

FEATURE_ORDER = [
    "having_IP_Address",
    "URL_Length",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "HTTPS_token",
    "Shortining_Service",
    "DNSRecord",
    "URL_of_Anchor"
]

class Predictor:

    def __init__(self):

        base_dir = os.path.dirname(os.path.dirname(__file__))

        model_dir = os.path.join(base_dir, "models")

        self.models = {

            "xgboost": joblib.load(
                os.path.join(model_dir, "xgboost.pkl")
            ),

            "lightgbm": joblib.load(
                os.path.join(model_dir, "lightgbm.pkl")
            )

        }

    # ==========================================================
    # Predict
    # ==========================================================

    def predict(self, features, model_name="xgboost"):

        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")

        model = self.models[model_name]

        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]

        confidence = model.predict_proba(features)[0]

        probability = float(max(confidence))

        return {

            "prediction": "Legitimate" if prediction == 1 else "Phishing",

            "confidence": round(probability * 100, 2),

            "model": model_name

        }