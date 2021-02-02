from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask('animal_sales')
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DATABASE', 'uri', fallback='sqlite:///animal_sales.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.get('DATABASE', 'track_modifications', fallback=False)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints import get_animal_center_bp
    app.register_blueprint(get_animal_center_bp())

    @app.before_request
    def force_json_content_type():
        if not request.is_json:
            abort(415)
    return app
