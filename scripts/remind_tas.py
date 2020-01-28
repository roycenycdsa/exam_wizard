import sys, os, ast, configparser
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
import pandas as pd

## Read from config file
config = configparser.ConfigParser()
config.read('structure_files/config.ini')
exam_path = config['exams']['path']
exam_name = config['exams']['name']

## Pull data into memory
wkld = pd.read_csv(exam_path + '/ta_exam_workload.csv')[['email', 'ta', 'workload']]
wkld['workload'] = wkld['workload'].apply(lambda l: [ast.literal_eval(l)])
wkld = wkld['workload'].apply(lambda x: pd.Series(x[0])) \
    .stack() \
    .reset_index(level=1, drop=True) \
    .to_frame('workload') \
    .join(wkld[['ta', 'email']], how='left')
wkld['workload'] = wkld['workload'].apply(lambda l: l[:24])
book = gb.read_grade_book(exam_name)
if not isinstance(book, pd.DataFrame):
    return book

## Find exams left to grade
graded = set(book['Student ID'].str.strip().values)
assigned = set(wkld['workload'].str.strip().values)
remaining = assigned - graded

## Identify TAs with work remaining
count = wkld[wkld['workload'].isin(remaining)].groupby('ta')['workload'].count()
wkld[wkld['workload'].isin(remaining)].groupby('ta')['workload']

## Send announcment to TAs
tas_remaining = wkld[wkld['workload'].isin(remaining)].groupby(['ta','email'])['workload'].apply(list).reset_index()
for ta in tas_remaining:
    tas_exams = ta['workload']






def remind_tas(exam_path, exam_name):
    ta_workload = exam_path + '/ta_exam_workload.csv'


    book = gb.read_grade_book(exam_name)
    if not isinstance(book, pd.DataFrame):
        return book

    submits = set([str(i) for i in pd.read_csv(exam_path + '/student_details.csv').student_id.values])
    graded = set(book['Student ID'].values)

    remain = list(submits - graded)
    if remain == []:
        print('All Exams have been graded!')
        return None
    to_send = pd.DataFrame([[i] + list(gb.assigned_to(i, ta_workload)) for i in remain]).groupby([1,2])[0].apply(list)
    to_send = to_send.reset_index()

    for i in range(to_send.shape[0]):
        name, email, tas_exams = to_send.iloc[i].values
        for j in range(len(tas_exams)):
            tas_exams[j] = list(filter(lambda l: os.path.splitext(l)[0] == tas_exams[j], os.listdir(exam_path)))[0]
        em = ml.create_attached_message(
            sender='charles.cohen@nycdatascience.com',
            to=email,
            subject='Exams Remain to be Graded',
            msg=f"You have {len(tas_exams)} exams\'s to grade. Please grade them promptly.\nUse the following form: {gb.get_link(exam_name)}",
            file_dir=exam_path,
            filenames=tas_exams
        )
        print('Message Written!!')
        #ml.send_message(em)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('structure_files/config.ini')
    path = config['exams']['path']
    name = config['exams']['name']
    remind_tas(path, name)
