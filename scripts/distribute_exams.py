import pandas as pd
import sys
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
from examwiz_pkg.examwiz_pkg.anon_app import anonymizer as an

def distribute(submissions_path, ta_details_path, form_link):
    # Delete any 'pre-anonymized' files from submissions_path
    an.fresh_start(submissions_path)

    # Anonymize exams
    anon_path, encryption_key = an.make_anon(submissions_path)
    active_tas = ml.get_ta_emails(ta_details_path)

    # Divy up workload and send TAs exams to grade
    workload = []
    num_exams = len(an.list_files(anon_path))
    for i in range(len(active_tas)):
        exams = an.list_files(anon_path)[(i * num_exams // len(active_tas)):((i + 1) * num_exams // len(active_tas))]
        workload.append({'ta': active_tas[i][0], 'workload': exams, 'email': active_tas[i][1]})
        em = ml.create_attached_message(
            sender='charles.cohen@nycdatascience.com',
            to=active_tas[i][1],
            subject='Exams to grade: R Midterm',
            msg=ml.grade_these(active_tas[i][0], form_link),
            file_dir=anon_path,
            filenames=exams
        )
        #print(ml.grade_these(active_tas[i][0], form_link))
        ml.send_message(em)
    pd.DataFrame(workload).to_csv(submissions_path + "/../ta_exam_workload.csv")

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
