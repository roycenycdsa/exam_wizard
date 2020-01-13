import sys
sys.path.append('..')
from examwiz_pkg.examwiz_pkg.gapi_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import pandas as pd


exam_id = input("Please enter in the ID of the gradebook you would like to make reports out of.\n")

gradebook = gb.read_grade_book(exam_id)

temp = input("Please enter the filename and path for the exam format (stored as .json).\n")

sample_exam = {"Question 1" : "Binary Search Question",
               "Question 2" : "Flatten a JSON",
               "Question 3" : "OOP: Fahrenheit to Celcius and Back",
               "Question 4" : "Calculate Machine Learning Coefficients",
               "Question 5" : "Python Data Analysis"}

exam_name = input("Please enter the exam name.\n")

rp.process_gradebook(gradebook, sample_exam, exam_name)
