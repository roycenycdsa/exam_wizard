import os, sys, shutil, re
from datetime import datetime as dt
import numpy as np
import pandas as pd


def list_files(loc):
    return os.listdir(loc)

def make_anon(loc):
    main_path = os.getcwd()
    os.chdir(loc + '/..')
    try:
        os.mkdir('./anon_student_exams')
    except FileExistsError:
        pass
    os.chdir(main_path)
    new_path = loc + '/../anon_student_exams'
    conversion = []



    for file in list_files(loc):
        temp_id = np.random.randint(1000, 9999)
        file_type = file[re.search('[.]', file).span()[0]:]
        new_file = new_path + '/' + str(temp_id) + file_type
        while os.path.exists(new_file) == True:
            temp_id = np.random.randint(1000, 9999)
            new_file = new_path + '/' + str(temp_id) + file_type
        conversion.append({'orig': loc + '/' + file, 'new': new_file, 'temp_id': str(temp_id),
                           'time': dt.now()})
        shutil.copy(src=loc + '/' + file, dst=new_file)
    conversion_key = loc + '/../conversion_key.csv'
    pd.DataFrame(data=conversion).to_csv(conversion_key, mode='a')
    return new_path, conversion_key


def read_key(key_path):
    return pd.read_csv(key_path)