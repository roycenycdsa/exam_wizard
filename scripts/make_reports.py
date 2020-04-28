import sys
import pandas as pd
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.rprt_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import configparser

#######################################################################
# get the sub_path from command line arguments
sub_path = sys.argv[1]
sub_path = r'{}'.format(sub_path)

# Get the config file of the exam
config = configparser.ConfigParser()
config.read(sub_path + '/config.ini')

# Get the name of the exam
exam_name = config['exams']['name']

# Get the gradebook file ID
file_id = config['exams']['gradebook']

#######################################################################
# load the gradebook by exam_name defunct
#gradebook = gb.read_grade_book(exam_name)

# load the gradebook by google sheet id
gradebook = gb.read_by_id(file_id)

# load the gradebook by local filepath
#gradebook = pd.read_csv('C:\\NYCDSA\\exams\\BDS021\\First_Midterm\\R_Midterm\\BDS021_R_Midterm.csv')

#######################################################################
# load the student details
student_key = pd.read_csv(sub_path + '/student_details.csv')

# load the exam details
exam_details = pd.read_json("./structure_files/exam_details.json")

# load the sample exam
sample_exam = exam_details[exam_details['name'] == exam_name]['structure'].values

# process the gradebook
rp.process_gradebook(gradebook = gradebook, student_keys = student_key,
                     exam_str = sample_exam, path = sub_path)
