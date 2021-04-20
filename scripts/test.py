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

#
# #config.readfp(io.BytesIO(sample_config))
#
#
#
# # List all contents
# print("List all contents")
# for section in config.sections():
#     print("Section: %s" % section)
#     for options in config.options(section):
#         print("x %s:::%s:::%s" % (options,
#                                   config.get(section, options),
#                                   str(type(options))))
#
# # Print some contents
# print("\nPrint some contents")
# print(config.get('other', 'use_anonymous'))  # Just get the value
# print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?