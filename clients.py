# clients.py
import requests
import json
import random
import multiprocessing

from app import NORMAL_USERS

HOST = "localhost:8080"


def run(i):
    r = random.uniform(0, 1)
    if r < 0.1:
        run_admin()
    else:
        run_normal_user()

def run_normal_user():
    # flow: /login, /protected (anchor), /record
    user = random.choice(NORMAL_USERS)
    login_payload = {'username': user, 'password': 'test'}
    access_token, status_code = run_login(login_payload)
    run_protected(access_token)
    user_record = get_user_record(access_token)
    print(f'{user} successfully accessed his/her data {user_record}')

def run_admin():
    # flow: /login, /protected (anchor), /records
    user = 'admin'
    login_payload = {'username': user, 'password': 'test'}
    access_token, status_code = run_login(login_payload)
    run_protected(access_token)
    admin_records = get_admin_records(access_token)
    print(f'{user} successfully accessed all records: {admin_records}')

def run_with_access_token(endpoint, access_token):
    headers = {"Authorization": f'Bearer {access_token}'}
    resp = requests.get(endpoint, headers=headers)
    return json.loads(resp.content)

def get_admin_records(access_token):
    return run_with_access_token(f'http://{HOST}/records', access_token)

def run_protected(access_token):
    return run_with_access_token(f'http://{HOST}/protected', access_token)

def run_clients(login_payload):
    access_token, status_code = run_login(login_payload)
    protected_resp = run_protected(access_token)
    print(f'/protected resp: {protected_resp}')
    user_record_resp = get_user_record(access_token)
    print(f'/record resp: {user_record_resp}')

def get_user_record(access_token):
    return run_with_access_token(f'http://{HOST}/record', access_token)

def run_login(login_payload):
    resp = requests.post(f'http://{HOST}/login', json=login_payload)
    try:
        content = resp.content
        json_data = json.loads(content)
        access_code = json_data['access_token']
        return access_code, resp.status_code
    except:
        return None, resp.status_code

p = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
p.map_async(run, range(100))
p.close()
p.join()





