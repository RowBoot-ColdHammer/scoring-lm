import os
import pandas as pd 
import sqlite3

# Path configurations
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)

data_dir = os.path.join(project_root, 'data')
db_dir = os.path.join(data_dir, 'db')
csv_dir = os.path.join(data_dir, 'csv')

sqlite_db = os.path.join(db_dir, 'test.db')
data_file = os.path.join(csv_dir, 'test_input_data.csv')


# conn = sqlite3.connect(sqlite_db)
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS customers (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         age INTEGER,
#         income REAL,
#         education BOOLEAN,
#         work BOOLEAN,
#         car BOOLEAN,
#         "default" INTEGER
#     )
# ''')
# conn.commit()
# conn.close()


data = pd.read_csv(data_file)

conn = sqlite3.connect(sqlite_db)
data.to_sql('customers', conn, if_exists='replace', index=False)
conn.close() 

# try:
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO customers (age, income, education, work, car, "default")
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (
#         request['age'],
#         request['income'],
#         request['education'],
#         request['work'],
#         request['car'],
#         default_pred
#     ))
#     conn.commit()
# finally:
#     conn.close()