import pandas as pd
import configparser
import sys

## This script takes the directory of the submissions files
## Locates the jsonMap.json containing the submission encryption key
## And generates the student_details.csv to be used by the exam_wizard

#sub_path = sys.argv[1]
#sub_path = r'{}'.format(sub_path)

sub_path = 'C:\\NYCDSA\\Exams\\BDS021\\First Midterm\\Python Midterm'

## Read json of student details
df = pd.read_json(sub_path + '\\jsonMap.json').T
df = df[df.role == 'user']

## Generate student_details.csv
df = df.reset_index()[['email', 'name', 'index']]
df = df.rename(columns={"index":"student_id"})
print(df)
df.to_csv(sub_path + '\\student_details.csv')
