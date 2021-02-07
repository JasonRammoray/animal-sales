from datetime import datetime, timedelta

from flask import jsonify, current_app, request, abort, make_response
from jsonschema import validate, ValidationError

from app import db
from app.blueprints import login_bp
import jwt

from app.models.animal_center import AnimalCenter
from app.models.api_access_request import ApiAccessRequest
from app.schemas.login_request import login_request_schema


@login_bp.route('', methods=['POST'])
def handle_login():
    json_payload = request.get_json()
    try:
        validate(instance=json_payload, schema=login_request_schema)
    except ValidationError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))
    login = json_payload.get('login', '')
    password = json_payload.get('password', '')
    animal_center = AnimalCenter.query.filter_by(login=login).first()
    invalid_credentials = not animal_center or not animal_center.check_password(password)
    if invalid_credentials:
        abort(make_response(jsonify({'error': 'invalid credentials'}), 401))
    current_app.logger.info(f'[POST] {request.url} center {animal_center.id} requested a token')

    api_request = ApiAccessRequest(center_id=animal_center.id)
    db.session.add(api_request)
    db.session.commit()

    token_eol = datetime.utcnow() + timedelta(hours=current_app.config['TOKEN_EXP_TIME'])
    message = {
        'sub': animal_center.id,
        'exp': token_eol
    }
    encoded_jwt = jwt.encode(message, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': encoded_jwt})
