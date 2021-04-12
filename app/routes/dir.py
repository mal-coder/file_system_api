import os
from datetime import datetime

from flask import Blueprint, request
from hurry.filesize import size

from app.authentication import authenticate
from app.helpers import prepare_path

bp = Blueprint('dir', __name__)


@bp.route('/dir/', methods=['GET'])
@authenticate
def get_dir(token_dir):
    path, request_path = prepare_path(token_dir, request.args.get('path', ''))
    try:
        dir_list = [
            {'name': entry.name,
             'is_file': entry.is_file(),
             'size': size(entry.stat().st_size),
             'created': datetime.fromtimestamp(entry.stat().st_ctime)} for entry in os.scandir(path=path)]
    except (FileNotFoundError, NotADirectoryError):
        return {'message': 'Directory not found'}, 404
    return {'path': request_path, 'dir': dir_list}, 200
