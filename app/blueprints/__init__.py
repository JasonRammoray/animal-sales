from flask import Blueprint

animal_center_bp = Blueprint('animal_center_bp', __name__, url_prefix='/register')


def get_animal_center_bp():
    from app.blueprints import animal_center
    return animal_center_bp
