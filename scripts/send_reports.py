import sys, os, time
sys.path.append('.')
import pandas as pd
from examwiz_pkg.examwiz_pkg.rprt_app import reporter as rp
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
import configparser


if __name__ == '__main__':
    # Access the file path of the exam
    sub_path = sys.argv[1]
    sub_path = r'{}'.format(sub_path)

    # Access the name of the exam
    config = configparser.ConfigParser()
    config.read(sub_path + '/config.ini')
    exam_name = config['exams']['name']
    admin_email = config['exams']['admin_email']

    report_path = sub_path + '/reports/'
    student_contact = sub_path + '/student_details.csv'

    df = pd.read_csv(student_contact)

    num_submissions = df.shape[0]

    idx = 0

    for i in range(num_submissions):
        # update the counter
        idx += 1

    	# extract the row of the particular student 
        std = df.iloc[i]

        # access the report of the students
        # we extract the name of the student as the filename
        names = std['name'].split()
        separator = '_'
        filename = separator.join(names)

        a = filename + '.pdf'
        b = std['name'].replace("'", "").lstrip()+'.pdf'
        #print(a, b)


        try:
            os.rename(report_path + a, report_path + b)
            try:
                # Create email message
                time.sleep(0.25)
                em = ml.create_attached_message(
                    sender = admin_email,
                    to = std.email.strip(),
                    subject = f'{exam_name} Grade Report',
                    msg = f'Hello {std["name"]}\nAttached is your Grade Report for {exam_name}\nPlease contact your grading TA with any questions.',
                    file_dir = report_path,
                    filenames = [b])

                # Send emails out
                ml.send_message(em)
                os.rename(report_path + b, report_path + a)
                print('Report sent to:', std['name'])
                print('Sent {} of {} report.'.format(idx, num_submissions + 1))
            except FileNotFoundError:
                print('Report not found for:', std["name"])
                os.rename(report_path + b, report_path + a)
        except FileNotFoundError:
            print('Report not found for:', std['name'])
            continue
