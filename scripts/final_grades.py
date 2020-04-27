import sys, configparser
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import pandas as pd


sub_path = sys.argv[1]
sub_path = r'{}'.format(sub_path)

# Get the config file of the exam
config = configparser.ConfigParser()
config.read(sub_path + '/config.ini')

exam_name = config['exams']['name']

file_id = config['exams']['gradebook']

#book = gb.read_grade_book(exam_name)

book = gb.read_by_id(file_id)

key = pd.read_csv(sub_path + '/student_details.csv')

question_cols = list(filter(lambda l: 'Comment' not in l and ('Question' in l or 'Problem' in l), book.columns))
book['Final Grade'] = book[question_cols].astype('int32').sum(axis=1)
book = book[['Student ID', 'Final Grade']]

df = pd.merge(left=book, right=key, left_on='Student ID', right_on='student_id', how='right').sort_values('Final Grade', ascending=False)
df[['name', 'Final Grade']].to_csv(sub_path + '/' + exam_name + '_final_grades.csv')