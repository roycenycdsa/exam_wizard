from ..gapi_utils import ml_service, dv_service

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from apiclient import errors

import mimetypes
import base64

def create_message(to, subject, message_text):
    """
    Generate the email message (no attachment)
    :param to: string - recipients email address
    :param subject: string - email header
    :param message_text: string - email body
    :return: dictionary containing raw message
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = ml_srvice.sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def create_attached_message(to, subject, message_text, file_dir, filename):
    """
    Generate the email message (with attachement)
    :param to: string - recipients email address
    :param subject: string - email header
    :param message_text: string - email body
    :param file_dir: string - location of attachment file
    :param filename: string - name of file
    :return: dictionary containing raw message
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = self.sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
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

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(message):
    """
    Sends email to recepient
    :param message: dictionary containing raw message
    """
    try:
        message = (mail_srvice.service.users().messages().send(userId='me', body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)