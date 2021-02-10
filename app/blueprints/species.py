from flask import current_app, request, abort, make_response, jsonify, g
from jsonschema import validate, ValidationError

from app import db
from app.blueprints import species_bp
from app.models.species import Species
from app.schemas.species import species_payload_schema
from app.utils.jwt_protected import jwt_protected


def get_species_repr(species_instance):
    return {
        'id': species_instance.id,
        'name': species_instance.name,
        'animals': len(species_instance.animals)
    }


def get_animal_repr(animal_instance):
    return {
        'id': animal_instance.id,
        'name': animal_instance.name,
        'species': animal_instance.species
    }


@species_bp.route('', methods=['POST'])
@jwt_protected
def add_species():
    current_app.logger.info(f'[POST] {request.url} center {g.entity_id} creates species')
    json_payload = request.get_json()
    try:
        validate(instance=json_payload, schema=species_payload_schema)
    except ValidationError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    instance = Species.query.filter_by(name=json_payload['name']).first()
    if instance is not None:
        abort(make_response(jsonify({'error': 'species already exists'}), 400))

    new_species = None
    try:
        new_species = Species(
            name=json_payload['name'],
            description=json_payload['description'],
            price=json_payload['price']
        )
    except AssertionError as err:
        abort(make_response(jsonify({'error': str(err)}), 400))

    db.session.add(new_species)
    db.session.commit()
    instance = Species.query.get(new_species.id)
    response = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'price': instance.price,
    }
    return jsonify(response), 201


@species_bp.route('', methods=['GET'])
def fetch_species():
    order_criteria = Species.id.asc()
    species = [
        get_species_repr(species)
        for species in Species.query.order_by(order_criteria).all()
    ]
    return jsonify(species), 200


@species_bp.route('/<species_id>', methods=['GET'])
def fetch_species_details(species_id):
    species = Species.query.get(species_id)
    if species is None:
        abort(make_response(jsonify({'error': 'species does not exist'}), 404))
    payload = {
        'id': species.id,
        'name': species.name,
        'description': species.description,
        'animals': [
            get_animal_repr(animal)
            for animal in sorted(species.animals, key=lambda item: item.id)
        ]
    }
    return jsonify(payload), 200
