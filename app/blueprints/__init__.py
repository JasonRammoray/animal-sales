from flask import Blueprint

registration_bp = Blueprint('registration_bp', __name__, url_prefix='/register')
animal_center_bp = Blueprint('animal_center_bp', __name__, url_prefix='/centers')
login_bp = Blueprint('login_bp', __name__, url_prefix='/login')


def get_registration_bp():
    from app.blueprints import registration
    return registration_bp


def get_animal_center_bp():
    from app.blueprints import animal_center
    return animal_center_bp


def get_login_bp():
    from app.blueprints import login
    return login_bp
