```## Model Training Output```

PS C:\Users\sweth\ai-honeypot-1> python src/train_ai_model.py
Starting the main block of train_ai_model.py...
Columns in the DataFrame (start of preprocess): Index(['timestamp', 'type', 'command', 'label', 'path'], dtype='object')
Value counts of labels before mapping:
 label
malicious    2
benign       1
Name: count, dtype: int64
Value counts of labels after mapping (including -1 for unknown):
 label_numerical
1    2
0    1
Name: count, dtype: int64
Data types of features before handling:
 timestamp          float64
type                object
command             object
label               object
path                object
label_numerical      int64
dtype: object
Columns after processing lists: Index(['timestamp', 'type', 'command', 'label', 'path', 'label_numerical'], dtype='object')
Columns after one-hot encoding: Index(['timestamp', 'label', 'label_numerical', 'type_command_execution',     
       'type_file_access', 'command_ls pwd rm -rf / netstat -an',
       'command_nan', 'path_/tmp/test.txt /etc/passwd /var/log/auth.log',
       'path_nan'],
      dtype='object')
Columns after dropping original categorical columns: Index(['timestamp', 'label_numerical', 'type_command_execution',
       'type_file_access', 'command_ls pwd rm -rf / netstat -an',
       'command_nan', 'path_/tmp/test.txt /etc/passwd /var/log/auth.log',
       'path_nan'],
      dtype='object')
Shape of features after one-hot encoding: (3, 8)       
Data types of features after encoding:
 timestamp                                           float64
label_numerical                                       int64
type_command_execution                                 
bool
type_file_access                                       
bool
command_ls pwd rm -rf / netstat -an                    
bool
command_nan                                            
bool
path_/tmp/test.txt /etc/passwd /var/log/auth.log       bool
path_nan                                               
bool
dtype: object
Number of valid samples: 3
Unique valid labels: [1 0]
Starting the train_model function...
Shape of X_train: (2, 6)
Shape of X_test: (1, 6)
Unique labels in y_train: [0 1]
Unique labels in y_test: [1]
Accuracy on the test set: 1.0000
Classification Report:
               precision    recall  f1-score   support 

   malicious       1.00      1.00      1.00         1  

    accuracy                           1.00         1  
   macro avg       1.00      1.00      1.00         1
weighted avg       1.00      1.00      1.00         1


Feature Importances:
path_nan: 0.2308
type_command_execution: 0.1923
command_ls pwd rm -rf / netstat -an: 0.1538
command_nan: 0.1538
path_/tmp/test.txt /etc/passwd /var/log/auth.log: 0.1538
type_file_access: 0.1154
Exiting the train_model function.
Trained model saved as honeypot_model.joblib
Label map: {'benign': 0, 'malicious': 1, 'exploit': 2}