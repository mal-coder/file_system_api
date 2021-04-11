import flask

from app.config import ROOT_PATH


def validate_body(func):
    def validation():
        if not flask.request.get_json():
            return {'message': 'Body not in JSON format'}, 400
        return func()

    return validation


def prepare_path(token_dir, path):
    request_path = normalize_path_name(path)
    dir_path = f'{ROOT_PATH}{token_dir}/{request_path}'
    return dir_path, request_path


def normalize_path_name(path):
    if path:
        if path[-1] != '/':
            return f'{path}/'
    return path
