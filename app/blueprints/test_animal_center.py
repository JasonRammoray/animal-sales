from app import db
from app.blueprints.animal_center import get_animal_center_repr, get_animal_repr


def test_should_provide_list_of_existing_animal_centers(client, animal_center, another_animal_center):
    expected_animal_centers = sorted([
        get_animal_center_repr(another_animal_center),
        get_animal_center_repr(animal_center)
    ], key=lambda center: center['id'])
    resp = client.get('/centers')
    assert resp.json == expected_animal_centers


def test_should_provide_empty_list_if_no_centers_added(client):
    resp = client.get('/centers')
    assert resp.json == []


def test_should_provide_animal_center_details(client, animal, another_animal, animal_center):
    animal.center_id = animal_center.id
    another_animal.center_id = animal_center.id
    db.session.commit()
    resp = client.get(f'/centers/{animal_center.id}')
    animals = sorted([another_animal, animal], key=lambda pet: pet.id)
    assert resp.json == {
        **get_animal_center_repr(animal_center),
        'animals': [get_animal_repr(animal) for animal in animals]
    }


def test_should_not_provide_details_for_non_existing_center(client):
    resp = client.get('/centers/99999')
    assert resp.status_code == 404
    assert resp.json == {'error': 'animal center does not exist'}
