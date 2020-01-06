from ..gapi_utils import st_service, dv_service, ap_service, ml_service
from apiclient import errors
import pandas as pd


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