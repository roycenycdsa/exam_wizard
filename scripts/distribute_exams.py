import pandas as pd
import sys, os, glob
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
from examwiz_pkg.examwiz_pkg.anon_app import anonymizer as an

def distribute(submissions_path, ta_details_path, form_link):
    encryption_key = submissions_path + '/student_details.csv'
    tas = ml.get_ta_emails(ta_details_path)

    # Divy up workload and send TAs exams to grade
    workload = []
    submissions = list(filter(lambda l: l not in ['student_details.csv', 'reports', '.DS_Store'], an.list_files(submissions_path)))
    num_submits = len(submissions)

    for i in range(len(tas)):
        exams = submissions[(i * num_submits // len(tas)):((i + 1) * num_submits // len(tas))]
        workload.append({'ta': tas[i][0], 'workload': exams, 'email': tas[i][1]})
        em = ml.create_attached_message(
            sender='charles.cohen@nycdatascience.com',
            to=tas[i][1],
            subject='Exams to grade: R Midterm',
            msg=ml.grade_these(tas[i][0], form_link),
            file_dir=submissions_path,
            filenames=exams
        )
        ml.send_message(em)


    pd.DataFrame(workload).to_csv(submissions_path + "/ta_exam_workload.csv")

if __name__ == '__main__':
    ask = False
    if ask:
        sub_path = input("Path to student submissions: ")
        ta_path = input("Path to TA contact details: ")
        form_link = input("Link to grading form: ")
    else:
        sub_path = 'demo/example_exam/student_submissions'
        ta_path = 'structure_files/TA_contact.txt'
        form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSdeOgHuin1UD9vCmjezzF0C7rF5h7nUz9RPqLMblcEBlv8i6g/viewform'

    distribute(sub_path, ta_path, form_link)
