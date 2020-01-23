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

gradebook = gb.read_grade_book(exam_name)

student_key = pd.read_csv(path + '/student_details.csv")

sample_exam = {"Question 1" : "Binary Search Question",
               "Question 2" : "Flatten a JSON",
               "Question 3" : "OOP: Fahrenheit to Celcius and Back",
               "Question 4" : "Calculate Machine Learning Coefficients",
               "Question 5" : "Python Data Analysis"}


rp.process_gradebook(gradebook, student_key, sample_exam, exam_name)
