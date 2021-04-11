import os

from flask import Blueprint, request

from app.authentication import authenticate
from app.helpers import prepare_path, validate_body

bp_file = Blueprint('delete_file', __name__)
bp_dir = Blueprint('delete_dir', __name__)


@bp_file.route('/delete/file/', methods=['DELETE'])
@validate_body
@authenticate
def delete_file(token_dir):
    path, request_path = prepare_path(token_dir, request.json.get('path', ''))
    request_filename = request.json.get('filename')
    if not request_filename:
        return {'message': 'File name not provided'}, 400
    path = f'{path}{request_filename}'
    if os.path.exists(path):
        os.remove(path)
    else:
        return {'message': 'File not found'}, 404
    return {'message': 'OK'}, 200


@bp_dir.route('/delete/dir/', methods=['DELETE'])
@validate_body
@authenticate
def delete_dir(token_dir):
    path, request_path = prepare_path(token_dir, request.json.get('path', ''))
    request_dirname = request.json.get('dirname')
    if not request_dirname:
        return {'message': 'Directory name not provided'}, 400
    path = f'{path}{request_dirname}'
    if os.path.exists(path):
        try:
            os.rmdir(path)
        except OSError as e:
            if e.errno == 66:
                return {'message': 'Directory not empty'}, 400
            else:
                raise
    else:
        return {'message': 'Directory not found'}, 404
    return {'message': 'OK'}, 200
