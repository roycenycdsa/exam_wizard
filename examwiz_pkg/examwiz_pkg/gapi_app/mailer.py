from ..gapi_utils import st_service, dv_service, ap_service, ml_service
from apiclient import errors
import base64, os, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import mimetypes
import email.encoders

def create_message(sender, to, subject, msg):
    message = MIMEText(msg)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def create_attached_message(sender, to, subject, msg, file_dir, filenames=[]):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(msg)
    message.attach(msg)

    for file in filenames:
        path = os.path.join(file_dir, str(file))
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        if main_type == 'text':
            fp = open(path, 'r')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'r')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'r')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
            message.attach(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=file)
        email.encoders.encode_base64(msg)
        message.attach(msg)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(message):
    try:
        message = ml_service.users().messages().send(userId='me', body=message).execute()
        print('Message Sent!')
    except errors.HttpError as error:
        print('An error occured: %s' % error)

def get_ta_emails(fp):
    names, emails = [], []
    with open(fp) as f:
        for ta in json.load(f):
            if ta['active'] == 'True':
                names.append(ta['name'])
                emails.append(ta['email'])
    return list(zip(names, emails))

def send_reminder(ta, exams, key, form_link):
    with open(key, 'r') as f:
        f.read

    msg = create_attached_message(
        sender='charles.cohen@nycdatascience.com',
        to=ta[0],
        subject='Exams remain to be graded',
        msg=f"""Hi {ta[1]},
You have exams that remain to be graded.
Please submit the grades here: {form_link}
If you received this email in error, please contact the bootcamp coordinator.""",
        file_dir='example_exam/anon_student_exams_perm/',
        filenames=exams
    )
    send_message(msg)

def grade_these(name, link):
    """Pre-Written Script 'grade these exams' for Mailer."""
    return f"Hi {name},\n" \
           f"Here are the R Midterm student exams.\n" \
           f"Please submit your grade to them promptly.\n" \
           f"Here is the submission form link: {link}"
