import os
import pandas as pd 

script_dir = os.path.dirname(__file__)

project_root = os.path.dirname(script_dir)  # Go up from utils/
data_dir = os.path.join(project_root, 'data')
csv_dir = os.path.join(data_dir, 'csv')

application_path = os.path.join(csv_dir, 'application_info.csv')
default_flg_path = os.path.join(csv_dir, 'default_flg.csv')


data = pd.read_csv(application_path)
defaultData = pd.read_csv(default_flg_path)

merged_df = pd.merge(data, defaultData, on='id', how='inner')

merged_df.rename(columns={
    'education_cd' : 'education',
    'good_work_flg': 'work',
    'car_own_flg': 'car',
    'default_flg': 'default',
}, inplace=True)

merged_data_slice = merged_df.get([ 'id', 'age', 'income', 'education', 'work', 'car', 'default'])

merged_data_slice['car'] = merged_data_slice['car'].replace({'Y': 1, 'N': 0})
merged_data_slice['education'] = merged_data_slice['education'].apply(lambda x: 1 if x == 'GRD' else 0)
merged_data_slice['income'] = merged_data_slice['income'].floordiv(1000)


# Save to new CSV
merged_data_slice.to_csv( os.path.join(csv_dir, 'test_input_data.csv'), index=False)