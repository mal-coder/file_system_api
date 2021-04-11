import hashlib

import flask

from app.config import ROOT_PWD, SALT
from app.models import Token


def authenticate_root(func):
    def authentication():
        token = flask.request.headers.get('Authorization')
        if not token or len(token.split()) != 2 or 'bearer' not in token.lower():
            return {'message': 'Authorization header missing or token in incorrect format'}, 400
        else:
            token = token.split()[1]
            if token == ROOT_PWD:
                return func()
            else:
                return {'message': 'Unauthorized'}, 401

    return authentication


def authenticate(func):
    def authentication():
        auth_token = flask.request.headers.get('Authorization')
        if not auth_token or len(auth_token.split()) != 2 or 'bearer' not in auth_token.lower():
            return {'message': 'Authorization header missing or token in incorrect format'}, 400
        else:
            auth_token = auth_token.split()[1].strip()
            token_hash = hashlib.md5((auth_token + SALT).encode()).hexdigest()
            token = Token.query.filter_by(token_hash=token_hash).first()
            if token:
                return func(token.root_dir)
            else:
                return {'message': 'Unauthorized'}, 401

    return authentication
