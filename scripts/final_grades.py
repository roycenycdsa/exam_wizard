import sys, configparser
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import pandas as pd

# getting the path of the file
sub_path = sys.argv[1]
sub_path = r'{}'.format(sub_path)

# Get the config file of the exam
config = configparser.ConfigParser()
config.read(sub_path + '/config.ini')

# get the name of the exams
exam_name = config['exams']['name']

# get the file_id of the gradebook so that we will be able to access the gradebook
file_id = config['exams']['gradebook']

#book = gb.read_grade_book(exam_name)

# get the gradebook
book = gb.read_by_id(file_id)

# load the student_details.csv file
key = pd.read_csv(sub_path + '/student_details.csv')

#print(book.columns)

question_cols = list(filter(lambda l: 'Comment' not in l and ('Question' in l or 'Problem' in l or 'Step' in l or 'Subquestion' in l), book.columns))

#print(question_cols)

#book['Final Grade'] = book[question_cols].astype('int32').sum(axis=1)
book['Final Grade'] = book[question_cols].astype(float).sum(axis=1)
book = book[['Student ID', 'Final Grade']]

#print(book['Final Grade'])

df = pd.merge(left=book, right=key, left_on='Student ID', right_on='student_id', how='inner').sort_values('Final Grade', ascending=False)
df[['name', 'Final Grade']].reset_index(drop = True).to_csv(sub_path + '/' + exam_name + '_final_grades.csv')