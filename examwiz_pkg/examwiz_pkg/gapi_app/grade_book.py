from ..gapi_utils import st_service, dv_service, ap_service, ml_service
from apiclient import errors
import pandas as pd
import os, shutil, ast

def create_grade_book(name, in_domain=True):
    # Creates a new google spreadsheet to hold exam grades
    spreadsheet = {
        'properties': {
            'title': name
        }
    }
    spreadsheet = st_service.spreadsheets().\
        create(body=spreadsheet, fields='spreadsheetId').execute()
    file_id = spreadsheet.get('spreadsheetId')
    update_permissions(file_id, in_domain)
    print('File Created\nid: {0}\nurl: {1}'.format(
        file_id, spreadsheet.get('webViewLink')
    ))

    return file_id

def read_grade_book(file_id):
    result = st_service.spreadsheets().values().get(
        spreadsheetId=file_id, range='Form Responses 1').execute()
    return pd.DataFrame(columns=result['values'][0], data=result['values'][1:])

def get_metadata(file_id):
    return dv_service.files().get(fileId=file_id, fields='*').execute()

def update_permissions(file_id, in_domain=True):
    try:
        # Design permission of file
        if in_domain:
            new_permission = {
                'type': 'domain',
                'role': 'reader',
                'domain': 'nycdatascience.com',
                'allowFileDiscovery': False
            }
        else:
            new_permission = {
                'type': 'anyone',
                'role': 'reader'
            }
        permission = dv_service.permissions().create(
            fileId=file_id,
            body=new_permission
        ).execute()

        return dv_service.files().update(
            fileId=file_id, body={'permissionIds': [permission['id']]}).execute()
    except errors as e:
        print('Error Occured:', e)

def get_link(file_id, link_type='view'):
    if link_type == 'download':
        try:
            return get_metadata(file_id)['webContentLink']
        except KeyError:
            return get_link(file_id, link_type='view')
    else:
        return get_metadata(file_id)['webViewLink']

def send_form(link, ta_email, exams):
    pass

def fresh_start(path):
    if os.path.exists(path + '/anon_student_exams'):
        shutil.rmtree(path + '/anon_student_exams')
        os.remove(path + '/conversion_key.csv')
    return None

def needs_grading(file_id, key_path):
    df = read_grade_book(file_id)
    st = pd.read_csv(key_path)

    ids = set([str(i) for i in st['temp_id'].values])
    done = set([str(i) for i in df['Student ID'].values])

    return [int(i) for i in ids - done]

def assigned_tas(test_id, exam_id, wkld_path):
    # Given a test id and a gradebook, find the ta who is supposed to grade it.
    wkld = pd.read_csv(wkld_path)
    wkld['workload'] = wkld.apply(lambda l: [os.path.splitext(i)[0] for i in ast.literal_eval(l.workload)], axis=1)

