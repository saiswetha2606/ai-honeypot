```## Model Prediction Output```

PS C:\Users\sweth\ai-honeypot-1> python src/predict_model.py 
Starting the main block of predict_model.py...
Starting the predict_with_model function...
Columns in the new DataFrame (before encoding): Index(['timestamp', 'type', 'command', 'label', 'path'], dtype='object')
Columns in the new DataFrame (after encoding): Index(['type_command_execution', 'type_file_access',
       'command_ls pwd rm -rf / netstat -an', 'command_nan',
       'path_/tmp/test.txt /etc/passwd /var/log/auth.log', 'path_nan'],        
      dtype='object')
Raw Predictions (numerical): [1 0 1]
Predicted Labels (string): ['malicious', 'benign', 'malicious']
True Labels (numerical): [ 1.  0. -1.]
True Labels (string): ['malicious', 'benign', 'unknown']
Accuracy on new data: 1.0000
Classification Report on new data:
               precision    recall  f1-score   support

      benign       1.00      1.00      1.00         1
   malicious       1.00      1.00      1.00         1

    accuracy                           1.00         2
   macro avg       1.00      1.00      1.00         2
weighted avg       1.00      1.00      1.00         2

PS C:\Users\sweth\ai-honeypot-1> 