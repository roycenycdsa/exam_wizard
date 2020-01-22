import pandas as pd
import os
submissions_dir = input()


## Read json of student details
df = pd.read_json(submissions_dir + '/jsonMap.json').T
df = df[df.role == 'user']

## Generate student_details.csv
df = df.reset_index()[['email', 'name', 'index']]
df = df.rename(columns={"index":"student_id"})
print(df)
df.to_csv(submissions_dir + '/student_details.csv')
