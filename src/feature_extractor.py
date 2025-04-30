import json
from sklearn.feature_extraction import DictVectorizer

class FeatureExtractor:
    def __init__(self):
        self.vectorizer = DictVectorizer(sparse=False)
        self.is_fitted = False

    def extract_features(self, raw_activity):
        try:
            activity = json.loads(raw_activity)
            features = {}
            features["activity_type"] = activity.get("type", "unknown")
            features["user"] = activity.get("user", "unknown")
            features["path"] = activity.get("path", "unknown")
            features["command"] = activity.get("command", "unknown")
            features["port"] = activity.get("port", -1)
            features["result"] = activity.get("result", "unknown")

            # More advanced features can be added here (e.g., n-grams of commands)
            return features
        except json.JSONDecodeError:
            return {}

    def fit(self, raw_data_list):
        feature_dicts = [self.extract_features(item) for item in raw_data_list]
        self.vectorizer.fit(feature_dicts)
        self.is_fitted = True

    def transform(self, raw_data_list):
        if not self.is_fitted:
            raise ValueError("Feature extractor must be fitted first.")
        feature_dicts = [self.extract_features(item) for item in raw_data_list]
        return self.vectorizer.transform(feature_dicts)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()

if __name__ == "__main__":
    # Example usage
    data = [
        '{"type": "login_attempt", "user": "guest", "result": "failure", "label": "benign"}',
        '{"type": "command_execution", "command": "rm -rf /", "label": "malicious"}',
        '{"type": "network_scan", "port": 22, "label": "suspicious"}'
    ]
    extractor = FeatureExtractor()
    extractor.fit(data)
    features = extractor.transform(data)
    print("Features:\n", features)
    print("Feature Names:\n", extractor.get_feature_names())