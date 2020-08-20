import pandas as pd
import sys
import os
from jsonmerge import merge


## This script takes the directory of the submissions files
## Locates the jsonMap.json containing the submission encryption key
## And generates the student_details.csv to be used by the exam_wizard

### Define a function to process the json file
def parse_json(filepath, user = True):
	df = pd.read_json(filepath).T
	
	if user == True:
		df = df[df.role == 'user']
	
	df = df.reset_index()[['email', 'name', 'index']]
	df = df.rename(columns = {'index': 'student_id'})
	
	return df

### Define a function to find the difference between two dataframe
def df_difference(df1, df2):
	'''
	input: df1, df2
	output:
	'''
	
	return df2[~df2['student_id'].isin(df1['student_id'])]

### Merge the two json files into one json file. 
def merge_json():
	df1 = pd.read_json(sub_path + '/jsonMap.json')
	df2 = pd.read_json(sub_path + '/jsonMap (1).json')
	df = merge(df1, df2)
	return df

if __name__ == '__main__':
	sub_path = sys.argv[1]
	sub_path = r'{}'.format(sub_path)

	# check whether there exists the student_details.csv file
	if os.path.exists(sub_path + '/student_details.csv'):
		
		# load the existing student_details
		student_details = pd.read_csv(sub_path + '/student_details.csv', index_col = 0)
		#print(student_details)

		# Load the two json files of the student details
		df1 = parse_json(sub_path + '/jsonMap.json')

		try:
			# We can try to change this part!!!!
			df2 = parse_json(sub_path + '/jsonMap (1).json')
			
			# Find the newly added students and their details
			df_diff = df_difference(df1, df2)
			
			# Initialize the new column 'sent' for df_diff to indicate whether the report has been sent or not
			#df_diff.loc[:, 'sent'] = 0
			df_diff.insert(3, 'sent', 0, True)
			
			# Merge with student_details
			new_student_details = pd.concat([student_details, df_diff], axis=0).drop_duplicates().reset_index(drop = True)
			
			# save the updated student_details to a csv file
			new_student_details.to_csv(sub_path + '/student_details.csv')

			######################## Update the JSON file ######################### 
			#needs to remove jsonMap(1).json file
			updated_df = merge_json()

			# update the jsonmap.json file
			updated_df.to_json(sub_path + '/jsonMap.json')

			# remove the new jsonMap.json
			os.remove(sub_path + '/jsonMap (1).json')
		
		except ValueError:
			
			print('There is nothing to update.')
		# we also need to merge the jsonMap file
		
	# if there doesn't exist the student_details.csv file, we will create a new one. 
	else:
		df = parse_json(sub_path + '/jsonMap.json')
		#df.to_csv(sub_path + '/student_details.csv')
		
		# Initialize the new column to indicate whether the report has been sent or not
		df['sent'] = 0
		
		# save the student_details to a csv file
		df.to_csv(sub_path + '/student_details.csv')