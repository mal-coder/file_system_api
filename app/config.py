import os

ROOT_PATH = os.environ['ROOT_PATH']
if 'app' in ROOT_PATH.lower():
    raise KeyError('ROOT_PATH cannot contain string "app"')
DB_URI = os.environ['DB_URI']
SALT = os.environ['SALT']
ROOT_PWD = os.environ['ROOT_PWD']
DEBUG = os.environ['DEBUG']
