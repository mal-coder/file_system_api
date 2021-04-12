from app.db import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=True)
    token_hash = db.Column(db.String, unique=True, nullable=False)
    root_dir = db.Column(db.String, unique=True, nullable=False)
