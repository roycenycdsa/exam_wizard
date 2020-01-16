import sys, os
sys.path.append('.')
import pandas as pd
from examwiz_pkg.examwiz_pkg.rprt_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml


if __name__ == '__main__':
    #report_path = input("Filepath to reports")
    #student_contact = input("Path to student details")


    report_path = './demo/example_exam/student_submissions/reports/'
    student_contact = './demo/example_exam/student_submissions/student_details.csv'
    exam_name = 'Example Exam'

    df = pd.read_csv(student_contact)
for i in range(df.shape[0]):
    std = df.iloc[i]
    a = str(std['student_id'])+'.pdf'
    b = std['name'].replace("'", "").lstrip()+'.pdf'
    #os.rename(report_path + a, report_path + b)
    try:
        em = ml.create_attached_message(
            sender='charles.cohen@nycdatascience.com',
            to=std.email.strip(),
            subject=f'{exam_name} Grade Report',
            msg=f'Hello {std["name"]}\nAttached is your Grade Report for {exam_name}\nPlease contact your grading TA with any questions.',
            file_dir=report_path,
            filenames=[a])
        ml.send_message(em)
        #os.rename(report_path + b, report_path + a)
        print('Report sent to:', std['name'])
    except FileNotFoundError:
        print('Report not found for:', std["name"])
        os.rename(report_path + b, report_path + a)