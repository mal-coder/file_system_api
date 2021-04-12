import uuid

import pytest
from flask import json

from app.config import ROOT_PWD
from app.helpers import normalize_path_name
from run import app

access_token = None
token_name = None


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_validation_token_unauthorized(client):
    headers = {'Authorization': f'Bearer wrong-token'}
    payload = {'name': str(uuid.uuid4())}
    path = '/root/create_token/'
    response = client.post(path=path, json=payload, headers=headers)

    assert response.status_code == 401


def test_validation_bearer_key_missing(client):
    headers = {'Authorization': f'Not-Bearer wrong-token'}
    payload = {'name': str(uuid.uuid4())}
    path = '/root/create_token/'
    response = client.post(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'Authorization header missing or token in incorrect format' in response.data


def test_create_token_name_key_missing(client):
    headers = {'Authorization': f'Bearer {ROOT_PWD}'}
    payload = {'test': 'test'}
    path = '/root/create_token/'
    response = client.post(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'Name not provided' in response.data


def test_create_token_success(client):
    global access_token, token_name
    headers = {'Authorization': f'Bearer {ROOT_PWD}'}
    payload = {'name': str(uuid.uuid4())}
    path = '/root/create_token/'
    response = client.post(path=path, json=payload, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 201
    assert 'access_token' in data_json
    access_token = data_json['access_token']
    assert data_json['name'] == payload['name']
    token_name = data_json['name']


def test_create_token_name_not_unique(client):
    global token_name
    headers = {'Authorization': f'Bearer {ROOT_PWD}'}
    payload = {'name': token_name}
    path = '/root/create_token/'
    response = client.post(path=path, json=payload, headers=headers)

    assert response.status_code == 409
    assert b'Name is not unique' in response.data


def test_token_validation_wrong_token(client):
    headers = {'Authorization': f'Bearer wrong-token'}
    path = '/dir/'
    response = client.get(path=path, headers=headers)

    assert response.status_code == 401


def test_validation_no_json_payload(client):
    headers = {'Authorization': f'Bearer {ROOT_PWD}'}
    payload = {'test': 'test'}
    path = '/root/create_token/'
    response = client.post(path=path, data=payload, headers=headers)

    assert response.status_code == 400
    assert b'Body not in JSON format' in response.data


def test_get_dir_empty(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    query_parameters = "?path="
    path = '/dir/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 200
    assert len(data_json['dir']) == 0


def test_create_file_success(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'filename': 'test_file.txt'}
    path = '/create/'
    response = client.put(path=path, json=payload, headers=headers)

    assert response.status_code == 201


def test_create_file_filename_key_missing(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'no_filename': ''}
    path = '/create/'
    response = client.put(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'File name not provided' in response.data


def test_create_file_filename_key_empty(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'filename': ''}
    path = '/create/'
    response = client.put(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'File name not provided' in response.data


def test_get_dir_not_empty(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    query_parameters = "?path="
    path = '/dir/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 200
    assert len(data_json['dir']) == 1
    assert 'dir1' in data_json['dir'][0]['name']
    assert data_json['dir'][0]['is_file'] is False
    assert 'created' in data_json['dir'][0]
    assert 'size' in data_json['dir'][0]


def test_get_dir_inner_dir_with_file(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    query_parameters = "?path=dir1/dir2/dir3"
    path = '/dir/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 200
    assert len(data_json['dir']) == 1
    assert 'test_file.txt' in data_json['dir'][0]['name']
    assert data_json['dir'][0]['is_file'] is True
    assert 'created' in data_json['dir'][0]
    assert 'size' in data_json['dir'][0]


def test_details_file(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    query_parameters = "?path=dir1/dir2/dir3&filename=test_file.txt"
    path = '/details/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'test_file.txt' in data_json['filename']
    assert 'created' in data_json['details']
    assert 'size' in data_json['details']


def test_delete_dir_dont_exist(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir10',
               'dirname': 'dir20'}
    path = '/delete/dir/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 404
    assert b'Directory not found' in response.data


def test_delete_dir_not_empty(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2',
               'dirname': 'dir3'}
    path = '/delete/dir/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'Directory not empty' in response.data


def test_delete_dirname_missing(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2',
               'dirname': ''}
    path = '/delete/dir/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'Directory name not provided' in response.data


def test_delete_file_success(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'filename': 'test_file.txt'}
    path = '/delete/file/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 200

    query_parameters = "?path=dir1/dir2/dir3"
    path = '/dir/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert len(data_json['dir']) == 0


def test_delete_file_not_existent(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'filename': 'test_file.txt'}
    path = '/delete/file/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 404
    assert b'File not found' in response.data


def test_delete_filename_not_provided(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2/dir3',
               'filename': ''}
    path = '/delete/file/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 400
    assert b'File name not provided' in response.data


def test_delete_dir_success(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'path': 'dir1/dir2',
               'dirname': 'dir3'}
    path = '/delete/dir/'
    response = client.delete(path=path, json=payload, headers=headers)

    assert response.status_code == 200

    query_parameters = "?path=dir1/dir2"
    path = '/dir/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert len(data_json['dir']) == 0


def test_disk_usage(client):
    global access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    path = '/disk_usage/'
    response = client.get(path=path, headers=headers)

    data_json = json.loads(response.data)

    assert response.status_code == 200
    for key in ('free', 'used', 'total'):
        assert key in data_json.keys()
