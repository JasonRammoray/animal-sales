import logging

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
import os

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLiteConnection

db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask('animal_sales')
    app.config.update(config)
    db.init_app(app)
    migrate.init_app(app, db)

    if not app.testing:
        audit_log_path = config['AUDIT_LOG']
        audit_log_folder = audit_log_path.split('/')[0]
        if not os.path.exists(audit_log_folder):
            os.mkdir(audit_log_folder)
        file_handler = RotatingFileHandler(audit_log_path, maxBytes=5*1024*1024, backupCount=5)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)

    from app.blueprints import get_registration_bp, get_animal_center_bp, get_login_bp, get_species_bp
    app.register_blueprint(get_registration_bp())
    app.register_blueprint(get_animal_center_bp())
    app.register_blueprint(get_login_bp())
    app.register_blueprint(get_species_bp())

    @event.listens_for(Engine, 'connect')
    def enable_sqlite_fk_support(db_conn, _):
        # See details at https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
        if not isinstance(db_conn, SQLiteConnection):
            return
        cursor = db_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @app.before_request
    def force_json_content_type():
        if not request.is_json:
            abort(415)
    return app
