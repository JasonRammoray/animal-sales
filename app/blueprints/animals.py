from flask import current_app, request, g, abort, make_response, jsonify
from jsonschema import validate, ValidationError

from app import db
from app.blueprints import animals_bp
from app.models.animal_center import AnimalCenter
from app.models.animals import Animals
from app.models.species import Species
from app.schemas.animal_add_request import animal_add_payload_schema
from app.schemas.animal_update_request import animal_update_payload_schema
from app.utils.jwt_protected import jwt_protected


def get_animal_repr(animal_instance):
    """
    Creates a dict animal representation
    based on an animal instance
    :param animal_instance: Animals
    :return: dict
    """
    return {
        'id': animal_instance.id,
        'centerId': animal_instance.center_id,
        'name': animal_instance.name,
        'description': animal_instance.description,
        'age': animal_instance.age,
        'species': animal_instance.species,
        'price': animal_instance.price
    }


@animals_bp.route('', methods=['POST'])
@jwt_protected
def add_animal():
    current_app.logger.info(f'[POST] {request.url} center {g.entity_id} creates animal')
    json_payload = request.get_json()
    try:
        validate(instance=json_payload, schema=animal_add_payload_schema)
    except ValidationError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    species = Species.query.get(json_payload['species'])
    if not species:
        abort(make_response(jsonify({'error': 'animal cannot be attached to a non-existing species'}), 400))

    animal_center = AnimalCenter.query.get(json_payload['centerId'])
    if not animal_center:
        abort(make_response(jsonify({'error': 'animal cannot be attached to a non-existing center'}), 400))

    new_animal = None
    try:
        new_animal = Animals(
            center_id=json_payload['centerId'],
            name=json_payload['name'],
            description=json_payload.get('description', ''),
            age=json_payload['age'],
            species=json_payload['species'],
            price=json_payload.get('price', 0)
        )
    except AssertionError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    db.session.add(new_animal)
    db.session.commit()
    instance = Animals.query.get(new_animal.id)
    return jsonify(get_animal_repr(instance)), 201


def get_animal_on_center_behalf(animal_id, animal_center_id):
    """
    Fetches an animal and ensures its ownership
    by a requested center. If the animal doesn't exist
    or it's not owned by the center, raises an HTTPException
    :param animal_id: int
    :param animal_center_id: int
    :return: Animals
    """
    animal = Animals.query.get(animal_id)
    if animal is None:
        abort(make_response(jsonify({'error': 'animal does not exists'}), 404))

    if animal.center_id != animal_center_id:
        abort(make_response(jsonify({'error': 'animal does not belong to the center'}), 400))
    return animal


@animals_bp.route('/<animal_id>', methods=['PUT'])
@jwt_protected
def update_animal(animal_id):
    current_app.logger.info(f'[PUT] {request.url} center {g.entity_id} updates animal {animal_id}')

    animal = get_animal_on_center_behalf(animal_id, g.entity_id)
    json_payload = request.get_json()
    try:
        validate(instance=json_payload, schema=animal_update_payload_schema)
    except ValidationError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    try:
        # Allow partial updates
        for prop, val in json_payload.items():
            if prop == 'centerId':
                if AnimalCenter.query.get(val) is None:
                    abort(make_response(jsonify({'error': 'animal cannot be attached to a non-existing center'}), 400))
                animal.center_id = val
            elif prop == 'species':
                if Species.query.get(val) is None:
                    abort(make_response(jsonify({'error': 'animal cannot be attached to a non-existing species'}), 400))
                animal.species = val
            else:
                setattr(animal, prop, val)
    except AssertionError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    db.session.commit()
    instance = Animals.query.get(animal_id)
    return jsonify(get_animal_repr(instance)), 200


@animals_bp.route('/<animal_id>', methods=['DELETE'])
@jwt_protected
def delete_animal(animal_id):
    current_app.logger.info(f'[DELETE] {request.url} center {g.entity_id} deletes animal {animal_id}')

    animal = get_animal_on_center_behalf(animal_id, g.entity_id)
    Animals.query.filter_by(id=animal.id).delete()
    db.session.commit()
    return make_response('', 204)


@animals_bp.route('', methods=['GET'])
def fetch_animals():
    animals = [get_animal_repr(instance) for instance in Animals.query.order_by(Animals.id.asc()).all()]
    return jsonify(animals), 200


@animals_bp.route('/<animal_id>', methods=['GET'])
def fetch_animal_details(animal_id):
    animal = Animals.query.get(animal_id)
    payload, status = ({'error': 'animal not found'}, 404) if animal is None else (get_animal_repr(animal), 200)
    return jsonify(payload), status
