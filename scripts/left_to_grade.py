import sys, ast, configparser
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
import pandas as pd

"""This script identifies TAs who have exams remaining to grade"""

## Read from config file
config = configparser.ConfigParser()
config.read('structure_files/config.ini')
exam_path = config['exams']['path']
exam_name = config['exams']['name']


## Pull data into memory
wkld = pd.read_csv(exam_path + '/ta_exam_workload.csv')[['email', 'ta', 'workload']]
wkld['workload'] = wkld['workload'].apply(lambda l: [ast.literal_eval(l)])
wkld = wkld['workload'].apply(lambda x: pd.Series(x[0])) \
    .stack() \
    .reset_index(level=1, drop=True) \
    .to_frame('workload') \
    .join(wkld[['ta', 'email']], how='left')
wkld['workload'] = wkld['workload'].apply(lambda l: l[:24])
book = gb.read_grade_book(exam_name)
# if not isinstance(book, pd.DataFrame):
#     return book

## Find exams left to grade
graded = set(book['Student ID'].str.strip().values)
assigned = set(wkld['workload'].str.strip().values)
remaining = assigned - graded

## Print out TAs with outstanding work remaining
print("TAs with work remaining:")
print(wkld[wkld['workload'].isin(remaining)].groupby('ta')['workload'].count())
print("TAs who have finished:")
print(wkld[~wkld['workload'].isin(remaining)]['ta'].unique())