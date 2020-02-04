import sys
import pandas as pd
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.rprt_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import configparser

config = configparser.ConfigParser()
config.read('structure_files/config.ini')
exam_name = config['exams']['name']
sub_path = config['exams']['path']

#gradebook = gb.read_grade_book(exam_name)
gradebook = pd.read_csv(sub_path + "r_midterm.csv")

student_key = pd.read_csv(sub_path + 'student_details.csv')

exam_details = pd.read_json("./structure_files/exam_details.json")

sample_exam = exam_details[exam_details['name'] == exam_name]['structure'].values

rp.process_gradebook(gradebook = gradebook, student_keys = student_key,
                     exam_str = sample_exam, path = sub_path)
