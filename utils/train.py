
import os
import datetime
import sqlite3
import joblib
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

script_dir = os.path.dirname(__file__)

project_root = os.path.dirname(script_dir)

data_dir = os.path.join(project_root, 'data')
db_dir = os.path.join(data_dir, 'db')
models_dir = os.path.join(data_dir, 'models')

conn = sqlite3.connect(os.path.join(db_dir, 'test.db'))

# Read data from SQLite table
data = pd.read_sql_query("SELECT * FROM customers", conn)

# Close connection
conn.close()

X = data.drop(columns=['id', 'default']).values
y = data['default'].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# print(X_train.shape, X_test.shape)
# print(Y_train.shape, Y_test.shape)

model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

ct = datetime.datetime.now()
ts = ct.timestamp()

joblib.dump(model, os.path.join(models_dir, f"model_{ts}.pkl"))

y_pred = model.predict(X_test)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(f"Rejects: {y_pred.mean() * 100:.0f}%")
print(f"Success: {precision * 100:.0f}%")
print(f"Full: {recall * 100:.0f}%")