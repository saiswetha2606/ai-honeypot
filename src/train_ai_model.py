import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

def load_data(file_path):
    """Loads data from a JSON Lines file."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def preprocess_data(df):
    """Preprocesses the DataFrame for training."""
    print("Columns in the DataFrame (start of preprocess):", df.columns)
    label_map = {'benign': 0, 'malicious': 1, 'exploit': 2}
    df['label_numerical'] = df['label'].map(label_map).fillna(-1)
    print("Value counts of labels before mapping:\n", df['label'].value_counts())
    print("Value counts of labels after mapping (including -1 for unknown):\n", df['label_numerical'].value_counts())

    print("Data types of features before handling:\n", df.dtypes)

    # Handle lists in 'command' and 'path' by joining them
    df['command'] = df['command'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
    df['path'] = df['path'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

    print("Columns after processing lists:", df.columns)

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=['type', 'command', 'path'], prefix=['type', 'command', 'path'], dummy_na=False)

    print("Columns after one-hot encoding:", df.columns)

    # Drop the original categorical columns and the 'label' column
    columns_to_drop = ['type', 'command', 'path', 'label']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    print("Columns after dropping original categorical columns:", df.columns)

    print("Shape of features after one-hot encoding:", df.shape)
    print("Data types of features after encoding:\n", df.dtypes)

    # Drop rows with unknown labels (-1)
    df_valid = df[df['label_numerical'] != -1].copy()
    print("Number of valid samples:", len(df_valid))
    print("Unique valid labels:", df_valid['label_numerical'].unique())

    X = df_valid.drop(columns=['label_numerical', 'timestamp'], errors='ignore')
    y = df_valid['label_numerical']

    return X, y, label_map

def train_model(X, y, label_map):
    """Trains a RandomForestClassifier model."""
    print("Starting the train_model function...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Shape of X_train:", X_train.shape)
    print("Shape of X_test:", X_test.shape)
    print("Unique labels in y_train:", np.unique(y_train))
    print("Unique labels in y_test:", np.unique(y_test))

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy on the test set: {accuracy:.4f}")

    # Get the unique labels present in y_test
    unique_test_labels = np.unique(y_test)
    # Create a list of target names corresponding to those labels
    target_names = [key for key, value in label_map.items() if value in unique_test_labels]

    print("Classification Report:\n", classification_report(y_test, y_pred, target_names=target_names, zero_division=0))

    # Feature Importance
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_names = X_train.columns
        feature_importance_dict = dict(zip(feature_names, importances))
        sorted_feature_importance = sorted(feature_importance_dict.items(), key=lambda item: item[1], reverse=True)
        print("\nFeature Importances:")
        for feature, importance in sorted_feature_importance:
            print(f"{feature}: {importance:.4f}")
    else:
        print("\nModel does not support feature importance analysis.")

    print("Exiting the train_model function.")
    return model

if __name__ == "__main__":
    print("Starting the main block of train_ai_model.py...") # Added print statement
    data = load_data('training_data.jsonl')
    X, y, label_map = preprocess_data(data.copy())
    trained_model = train_model(X, y, label_map)
    joblib.dump(trained_model, 'honeypot_model.joblib')
    print("Trained model saved as honeypot_model.joblib")
    print("Label map:", label_map)