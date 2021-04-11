import os

from flask import Blueprint, request

from app.authentication import authenticate
from app.helpers import prepare_path, validate_body

bp = Blueprint('create', __name__)


@bp.route('/create/', methods=['PUT'])
@validate_body
@authenticate
def create(token_dir):
    path, request_path = prepare_path(token_dir, request.json.get('path', ''))
    request_filename = request.json.get('filename')
    if not request_filename:
        return {'message': 'File name not provided'}, 400
    content = ''
    if not os.path.exists(path):
        os.makedirs(path)
    # if os.path.exists(path + request_filename):
    #    return {'message': 'File already exists'}, 400
    with open(os.path.join(path, request_filename), 'w') as temp_file:
        temp_file.write(content)
    return {'message': 'Created'}, 201
