from app import db
from app.blueprints.animals import get_animal_repr
from app.models.animals import Animals


def test_should_add_animal(client, auth_http_headers, animal_center, species):
    payload = {
        'name': 'test animal 1',
        'description': 'the cutest animal ever',
        'price': 55.67,
        'centerId': animal_center.id,
        'species': species.id,
        'age': 2
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.json == {'id': 1, **payload}


def test_should_not_add_animal_with_invalid_center(client, auth_http_headers, species):
    payload = {
        'name': 'test animal 2',
        'price': 12.34,
        'centerId': 99999999,
        'species': species.id,
        'age': 3
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal cannot be attached to a non-existing center'}


def test_should_not_add_animal_with_invalid_species(client, auth_http_headers, animal_center):
    payload = {
        'name': 'test animal 3',
        'price': 56.78,
        'centerId': animal_center.id,
        'species': 99999999,
        'age': 4.1
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal cannot be attached to a non-existing species'}


def test_should_not_add_animal_with_invalid_name(client, auth_http_headers, animal_center, species):
    payload = {
        'name': 'tst4',
        'price': 3.14,
        'centerId': animal_center.id,
        'species': species.id,
        'age': 3.2
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert 'is too short' in resp.json['error']


def test_should_not_add_animal_with_invalid_age(client, auth_http_headers, animal_center, species):
    payload = {
        'name': 'Greenland shark',
        'price': 101.25,
        'description': 'https://en.wikipedia.org/wiki/Greenland_shark',
        'centerId': animal_center.id,
        'species': species.id,
        'age': 501
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert 'is greater than the maximum' in resp.json['error']


def test_should_not_add_animal_with_invalid_price(client, auth_http_headers, animal_center, species):
    payload = {
        'name': 'Green monkey racehorse',
        'price': 16000000,
        'description': 'https://en.wikipedia.org/wiki/The_Green_Monkey',
        'centerId': animal_center.id,
        'species': species.id,
        'age': 10
    }
    resp = client.post('/animals', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert 'is greater than the maximum' in resp.json['error']


def test_should_update_animal(client, animal, another_animal_center, another_species, auth_http_headers):
    assert animal.center_id != another_animal_center.id
    payload = {
        'name': animal.name[::-1],
        'age': 55,
        'price': 999.99,
        'description': animal.description[::-1],
        'centerId': another_animal_center.id,
        'species': another_species.id
    }
    resp = client.put(f'/animals/{animal.id}', json=payload, headers=auth_http_headers)
    assert resp.json == {'id': animal.id, **payload}


def test_should_not_update_animal_if_requesting_center_has_no_ownership(
        client, animal, another_animal_center,
        animal_center, auth_http_headers
):
    assert animal.center_id == animal_center.id
    animal.center_id = another_animal_center.id
    db.session.commit()
    payload = {
        'age': 55,
        'price': 999.99,
    }
    resp = client.put(f'/animals/{animal.id}', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal does not belong to the center'}


def test_should_not_update_animal_if_new_center_does_not_exists(client, animal, auth_http_headers):
    payload = {'centerId': 99999}
    resp = client.put(f'/animals/{animal.id}', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal cannot be attached to a non-existing center'}


def test_should_not_update_animal_if_new_species_does_not_exists(client, animal, auth_http_headers):
    payload = {'species': 99999}
    resp = client.put(f'/animals/{animal.id}', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal cannot be attached to a non-existing species'}


def test_should_not_update_non_existing_animal(client, auth_http_headers):
    payload = {'name': 'jumbo'}
    resp = client.put('/animals/999999', json=payload, headers=auth_http_headers)
    assert resp.status_code == 404
    assert resp.json == {'error': 'animal does not exists'}


def test_should_not_update_animal_with_empty_payload(client, auth_http_headers, animal):
    payload = {}
    resp = client.put(f'/animals/{animal.id}', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400


def test_should_delete_animal(client, auth_http_headers, animal):
    resp = client.delete(f'/animals/{animal.id}', headers=auth_http_headers)
    assert resp.status_code == 204
    assert Animals.query.get(animal.id) is None


def test_should_not_delete_animal_if_center_has_no_ownership(client, auth_http_headers, animal, another_animal_center):
    assert animal.center_id != another_animal_center.id
    animal.center_id = another_animal_center.id
    db.session.commit()
    resp = client.delete(f'/animals/{animal.id}', headers=auth_http_headers)
    assert resp.status_code == 400
    assert resp.json == {'error': 'animal does not belong to the center'}


def test_should_not_delete_non_existing_animal(client, auth_http_headers):
    resp = client.delete('/animals/99999', headers=auth_http_headers)
    assert resp.status_code == 404
    assert resp.json == {'error': 'animal does not exists'}


def test_should_provide_list_of_animals(client, animal, another_animal):
    resp = client.get('/animals')
    expected_list = sorted([get_animal_repr(another_animal), get_animal_repr(animal)], key=lambda val: val['id'])
    assert resp.json == expected_list


def test_should_provide_empty_list_when_no_animal_exists(client):
    resp = client.get('/animals')
    assert [] == resp.json


def test_should_provide_animal_details(client, animal):
    resp = client.get(f'/animals/{animal.id}')
    assert resp.json == get_animal_repr(animal)


def test_should_not_provide_details_on_non_existing_animal(client):
    resp = client.get('/animals/992342')
    assert resp.status_code == 404
    assert resp.json == {'error': 'animal not found'}
