import pandas as pd
import sys, os, time
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
from examwiz_pkg.examwiz_pkg.anon_app import anonymizer as an
import configparser


def distribute(submissions_path, ta_details_path, form_link, name):
    encryption_key = submissions_path + '/student_details.csv'
    json_map = submissions_path + '/jsonMap.json'
    tas = ml.get_ta_emails(ta_details_path)

    # Divy up workload and send TAs exams to grade
    workload = []
    not_exams = ['student_details.csv', 'reports', '.DS_Store', 'ta_exam_workload.csv', 'jsonMap.json']
    submissions = list(filter(lambda l: l not in not_exams,
                              an.list_files(submissions_path)))
    df = pd.read_json(json_map).T.reset_index()
    submissions = list(filter(lambda l: os.path.splitext(l)[0] in df[df.role=='user']['index'].values, os.listdir(submissions_path)))


    num_submits = len(submissions)

    for i in range(len(tas)):
        exams = submissions[(i * num_submits // len(tas)):((i + 1) * num_submits // len(tas))]
        workload.append({'ta': tas[i][0], 'workload': exams, 'email': tas[i][1]})
        time.sleep(0.25)
        em = ml.create_attached_message(
            sender='xiangwei.zhong@nycdatascience.com',
            to=tas[i][1],
            subject='Exams to grade: ' + name,
            msg=ml.grade_these(tas[i][0], form_link, name),
            file_dir=submissions_path,
            filenames=exams
        )
        #print(tas[i][0], exams)
        ml.send_message(em)
    pd.DataFrame(workload).to_csv(submissions_path + "/ta_exam_workload.csv")

if __name__ == '__main__':
    # Access the file path from command line argument
    sub_path = sys.argv[1]
    sub_path = r'{}'.format(sub_path)

    # Get the config file of the exam
    config = configparser.ConfigParser()
    config.read(sub_path + '/config.ini')

    # Get the name of the exam
    exam_name = config['exams']['name']

    # Get the TA contacts
    ta_path = 'structure_files/TA_contact.txt'
    
    # Attach the google survey form to the email
    #form_link = gb.get_link(exam_name)
    form_link = config['exams']['formlink']

    ## Verify that sub_path has not already been distributed.
    if os.path.exists(sub_path + '/ta_exam_workload.csv'):
        prompt = input('These exams have already been distributed to TAs.\nPress any key to exit.')
        if len(prompt) != 0:
            sys.exit()

    distribute(sub_path, ta_path, form_link, exam_name)
