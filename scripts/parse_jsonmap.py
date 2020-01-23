import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('structure_files/config.ini')
submissions_dir = config['exams']['path']

## This script takes the directory of the submissions files
## Locates the jsonMap.json containing the submission encryption key
## And generates the student_details.csv to be used by the exam_wizard


## Read json of student details
df = pd.read_json(submissions_dir + '/jsonMap.json').T
df = df[df.role == 'user']

## Generate student_details.csv
df = df.reset_index()[['email', 'name', 'index']]
df = df.rename(columns={"index":"student_id"})
print(df)
df.to_csv(submissions_dir + '/student_details.csv')
