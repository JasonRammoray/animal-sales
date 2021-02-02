from flask import jsonify, request, abort, make_response
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.blueprints import animal_center_bp
from app.models.animal_center import AnimalCenter
from app.schemas.animal_center import animal_center_payload_schema


@animal_center_bp.route('/', methods=['POST'])
def handle_animal_center_registration():
    json_payload = request.get_json()
    try:
        validate(instance=json_payload, schema=animal_center_payload_schema)
    except ValidationError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    instance = AnimalCenter.query.filter(AnimalCenter.login == json_payload['login']).first()
    if instance is not None:
        abort(make_response(jsonify({'error': 'login is occupied'}), 400))

    new_animal_center = AnimalCenter(
        login=json_payload['login'],
        address=json_payload['address']
    )
    new_animal_center.set_password(json_payload['password'])
    db.session.add(new_animal_center)
    db.session.commit()
    instance = AnimalCenter.query.get(new_animal_center.id)
    serialized = {
        'id': instance.id,
        'address': instance.address,
    }
    return jsonify(serialized), 201
