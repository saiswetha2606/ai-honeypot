import joblib
from feature_extractor import FeatureExtractor

class Detector:
    def __init__(self):
        print("AI Detector initialized.")
        try:
            self.model, self.feature_extractor = joblib.load("ai_model.joblib")
            print("Loaded trained AI model.")
        except FileNotFoundError:
            print("AI model file not found. Train the model first (train_model.py).")
            self.model = None
            self.feature_extractor = FeatureExtractor() # Initialize for rule-based

    def detect(self, activity):
        if self.model and self.feature_extractor.is_fitted:
            features = self.feature_extractor.transform([activity])
            prediction = self.model.predict(features)
            label_map_rev = {0: "benign", 1: "suspicious", 2: "malicious"}
            predicted_label = label_map_rev.get(prediction[0], "unknown")
            if predicted_label in ["suspicious", "malicious"]:
                return f"AI DETECTOR: Predicted activity as {predicted_label}"

        # Fallback to rule-based detection
        if "rm -rf /" in activity:
            return "RULE TRIGGERED: Attempt to delete all files!"
        elif "network_scan" in activity and "port 22" in activity:
            return "RULE TRIGGERED: Network scan on SSH port"
        # Add more rules as needed
        return None

def initialize_detector():
    print("AI Detector initialized.")
    return Detector()