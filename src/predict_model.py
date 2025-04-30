# src/predict_model.py
import json
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

# Load the label map from the training script (assuming it was printed)
label_map = {'benign': 0, 'malicious': 1, 'exploit': 2}
reverse_label_map = {v: k for k, v in label_map.items()}

def load_data(file_path):
    """Loads data from a JSON Lines file."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def load_new_data(file_path):
    """Loads new data from a JSON Lines file."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def preprocess_new_data(df, training_columns):
    """Preprocesses the new DataFrame for prediction."""
    print("Columns in the new DataFrame (before encoding):", df.columns)

    # Handle lists in 'command' and 'path' by joining them
    df['command'] = df['command'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
    df['path'] = df['path'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

    # One-hot encode categorical features, handling missing columns
    df = pd.get_dummies(df, columns=['type', 'command', 'path'], prefix=['type', 'command', 'path'], dummy_na=False)

    # Add missing columns from training data and fill with 0
    missing_cols = set(training_columns) - set(df.columns)
    for c in missing_cols:
        df[c] = 0

    # Ensure the order of columns is the same as in training
    df = df[training_columns]

    print("Columns in the new DataFrame (after encoding):", df.columns)
    return df

def get_training_columns(training_data_file='training_data.jsonl'):
    """Loads a bit of the training data to get the column names after preprocessing."""
    temp_df = load_data(training_data_file)
    temp_df['command'] = temp_df['command'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
    temp_df['path'] = temp_df['path'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
    temp_df = pd.get_dummies(temp_df, columns=['type', 'command', 'path'], prefix=['type', 'command', 'path'], dummy_na=False)
    columns_to_keep = [col for col in temp_df.columns if col not in ['label', 'timestamp', 'label_numerical']]
    return columns_to_keep

def predict_with_model(model_path='honeypot_model.joblib', new_data_file='new_honeypot_data.jsonl', training_data_file='training_data.jsonl'):
    """Loads the trained model, preprocesses new data, and makes predictions."""
    print("Starting the predict_with_model function...") # Added print statement
    loaded_model = joblib.load(model_path)
    training_columns = get_training_columns(training_data_file)
    new_df = load_new_data(new_data_file)
    X_new = preprocess_new_data(new_df.copy(), training_columns)
    X_new = X_new.drop(columns=['timestamp'], errors='ignore') # Ensure timestamp is not used for prediction

    if X_new is not None:
        predictions = loaded_model.predict(X_new)
        print("Raw Predictions (numerical):", predictions)

        predicted_labels = [reverse_label_map.get(p, 'unknown') for p in predictions]
        print("Predicted Labels (string):", predicted_labels)

        if 'label' in new_df.columns:
            true_labels = new_df['label'].map(label_map).fillna(-1)
            print("True Labels (numerical):", true_labels.values)
            true_labels_string = [reverse_label_map.get(l, 'unknown') for l in true_labels]
            print("True Labels (string):", true_labels_string)

            from sklearn.metrics import accuracy_score, classification_report
            known_mask = true_labels != -1
            y_true_known = true_labels[known_mask]
            y_pred_known = predictions[known_mask]

            if np.any(known_mask):
                accuracy = accuracy_score(y_true_known, y_pred_known)
                print(f"Accuracy on new data: {accuracy:.4f}")
                unique_true_labels_present = np.unique(y_true_known)
                target_names = [reverse_label_map[label] for label in unique_true_labels_present if label in reverse_label_map]
                print("Classification Report on new data:\n", classification_report(y_true_known, y_pred_known, target_names=target_names, zero_division=0))
            else:
                print("No true labels provided in the new data for evaluation.")

if __name__ == "__main__":
    print("Starting the main block of predict_model.py...") # Added print statement
    predict_with_model()