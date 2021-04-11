from flask import Flask

from app.config import DB_URI
from app.db import db
from app.routes import dir, details, disk_usage, delete, create, root


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(dir.bp)
        app.register_blueprint(details.bp)
        app.register_blueprint(disk_usage.bp)
        app.register_blueprint(delete.bp_file)
        app.register_blueprint(delete.bp_dir)
        app.register_blueprint(create.bp)
        app.register_blueprint(root.bp)

    return app
