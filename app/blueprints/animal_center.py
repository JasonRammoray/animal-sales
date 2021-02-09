from flask import jsonify, abort, make_response

from app.blueprints import animal_center_bp
from app.models.animal_center import AnimalCenter


def get_animal_center_repr(animal_center_instance):
    return {
        'id': animal_center_instance.id,
        'name': animal_center_instance.login
    }


def get_animal_repr(animal_instance):
    return {
        'id': animal_instance.id,
        'name': animal_instance.name,
        'species': animal_instance.species
    }


@animal_center_bp.route('', methods=['GET'])
def handle_animal_centers_fetch():
    order_criteria = AnimalCenter.id.asc()
    results = [
        get_animal_center_repr(animal_center)
        for animal_center in AnimalCenter.query.order_by(order_criteria).all()
    ]
    return jsonify(results), 200


@animal_center_bp.route('/<animal_center_id>', methods=['GET'])
def handle_animal_center_details_fetch(animal_center_id):
    animal_center = AnimalCenter.query.get(animal_center_id)
    if animal_center is None:
        abort(make_response(jsonify({'error': 'animal center does not exist'}), 404))

    animal_repr = get_animal_center_repr(animal_center)
    animal_repr['animals'] = [
        get_animal_repr(animal) for animal in
        sorted(animal_center.animals, key=lambda animal: animal.id)
    ]
    return jsonify(animal_repr), 200
