from ..gapi_utils import st_service, dv_service, ap_service, ml_service
from apiclient import errors
import pandas as pd
import os, ast, json

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

def read_by_id(file_id):
    result = st_service.spreadsheets().values().get(
        spreadsheetId=file_id, range='Form Responses 1').execute()

    # check the dimensions of the columns
    #print(result['values'][1:][0])

    num_col1 = len(result['values'][0])
    #print(num_col1)

    num_col2 = len(result['values'][1:][0])
    #print(num_col2)

    num_col = min(num_col1, num_col2)

    return pd.DataFrame(columns=result['values'][0][0:num_col], data=result['values'][1:])
    #return pd.DataFrame(result['values'][1:]).shape
    #return pd.DataFrame(data=result['values'][0]).shape
    #return len(result['values'][1:][0])

def read_grade_book(name):

    data = json.load(open('structure_files/exam_details.json', 'r'))
    try:
        file_id = list(filter(lambda l: l['name'] == name, data))[0]['gradebook']
    except IndexError:
        return 'Exam Name not Found. Retry or create Add New Exam'

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

def get_link(name):
    data = json.load(open('structure_files/exam_details.json', 'r'))
    try:
        return list(filter(lambda l: l['name'] == name, data))[0]['formlink']
    except IndexError:
        return 'Exam Name not Found. Retry or create Add New Exam'

def needs_grading(file_id, key_path):
    df = read_grade_book(file_id)
    st = pd.read_csv(key_path)

    ids = set([str(i) for i in st['temp_id'].values])
    done = set([str(i) for i in df['Student ID'].values])

    return [int(i) for i in ids - done]

def assigned_to(test_id, path):
    # Given a submission id and ta_workload path
    wkld = pd.read_csv(path)
    wkld['workload'] = wkld.apply(lambda l: [os.path.splitext(i)[0] for i in ast.literal_eval(l.workload)], axis=1)
    try:
        a = list(wkld[list(map(lambda l: str(test_id) in l, wkld['workload'].values))][['ta', 'email']].values[0])
        return a
    except IndexError as e:
        print(test_id + ' not found')
        return []


def get_file_path(test_id, key_path):
    df = pd.read_csv(key_path)
    return df.loc[df['temp_id'] == int(test_id)]['new'].iloc[0]



