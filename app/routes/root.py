import hashlib
import os
import uuid

from flask import Blueprint, request

from app.authentication import authenticate_root
from app.config import SALT, ROOT_PATH
from app.db import db
from app.helpers import validate_json_body
from app.models import Token

bp = Blueprint('create_token', __name__)


@bp.route('/root/create_token/', methods=['POST'])
@authenticate_root
@validate_json_body
def create_token():
    request_name = request.json.get('name')
    if not request_name:
        return {'message': 'Name not provided'}, 400
    if not Token.query.filter_by(name=request_name).all():
        new_dir = str(uuid.uuid4())
        token = str(uuid.uuid4())
        token_hash = hashlib.md5((token + SALT).encode()).hexdigest()

        new_token = Token(name=request_name, token_hash=token_hash, root_dir=new_dir)
        db.session.add(new_token)

        path = f'{ROOT_PATH}{new_dir}'
        os.makedirs(path)

        db.session.commit()
        return {'message': 'Created', 'access_token': token, 'name': request_name}, 201
    else:
        return {'message': 'Name is not unique'}, 409
