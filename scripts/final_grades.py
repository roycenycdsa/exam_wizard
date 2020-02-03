import sys, configparser
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import pandas as pd

config = configparser.ConfigParser()
config.read('structure_files/config.ini')
exam_name = config['exams']['name']
sub_path = config['exams']['path']

book = gb.read_grade_book(exam_name)
key = pd.read_csv(sub_path + '/student_details.csv')

question_cols = list(filter(lambda l: 'Comment' not in l and ('Question' in l or 'Problem' in l), book.columns))
book['Final Grade'] = book[question_cols].astype('int32').sum(axis=1)
book = book[['Student ID', 'Final Grade']]

df = pd.merge(left=book, right=key, left_on='Student ID', right_on='student_id', how='right').sort_values('Final Grade', ascending=False)
df[['name', 'Final Grade']].to_csv(sub_path + '/' + exam_name + '_final_grades.csv')