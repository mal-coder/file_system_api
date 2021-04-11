import os
from datetime import datetime

from flask import Blueprint, request
from hurry.filesize import size

from app.authentication import authenticate
from app.helpers import prepare_path, validate_body

bp = Blueprint('details', __name__)


@bp.route('/details/', methods=['GET'])
@validate_body
@authenticate
def get_details(token_dir):
    path, request_path = prepare_path(token_dir, request.json.get('path', ''))
    request_filename = request.json.get('filename')
    if not request_filename:
        return {'message': 'File name not provided'}, 400
    path = f'{path}{request_filename}'
    if os.path.exists(path):
        file_details = {'size': size(os.path.getsize(path)),
                        'created': datetime.fromtimestamp(os.path.getctime(path))}
        return {'path': request_path, 'filename': request_filename, 'details': file_details}, 200
    return {'message': 'File not found'}, 404
