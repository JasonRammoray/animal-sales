from flask import jsonify

from app.blueprints import animal_center_bp
from app.models.animal_center import AnimalCenter


@animal_center_bp.route('', methods=['GET'])
def handle_animal_centers_fetch():
    results = [{
        'id': animal_center.id,
        'name': animal_center.login
    } for animal_center in AnimalCenter.query.all()]
    return jsonify(results), 200
