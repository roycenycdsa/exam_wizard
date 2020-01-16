import sys
import pandas as pd
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.rprt_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb

#exam_id = input("Please enter the name of the gradebook you would like to make reports out of.\n")
exam_id = 'Example Exam'

gradebook = gb.read_grade_book(exam_id)

student_key = pd.read_csv("./demo/example_exam/student_submissions/student_details.csv")

sample_exam = {"Question 1" : "Binary Search Question",
               "Question 2" : "Flatten a JSON",
               "Question 3" : "OOP: Fahrenheit to Celcius and Back",
               "Question 4" : "Calculate Machine Learning Coefficients",
               "Question 5" : "Python Data Analysis"}

exam_name = 'Example Exam'
rp.process_gradebook(gradebook, student_key, sample_exam, exam_name)
