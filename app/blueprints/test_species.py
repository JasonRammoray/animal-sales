from app import db


def test_should_add_species(client, auth_http_headers):
    payload = {
        'name': 'test species',
        'description': 'test description',
        'price': 42.5
    }
    resp = client.post('/species', json=payload, headers=auth_http_headers)
    assert resp.json == {'id': 1, **payload}


def test_should_not_add_species_with_invalid_payload(client, auth_http_headers):
    payload = {'name': 'weirdo species'}
    resp = client.post('/species', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400


def test_should_not_add_already_existing_species_twice(client, auth_http_headers, species):
    payload = {
        'name': species.name,
        'description': 'British scientists discovered a new species',
        'price': 55.44
    }
    resp = client.post('/species', json=payload, headers=auth_http_headers)
    assert resp.status_code == 400


def test_should_provide_species_list(client, animal, another_animal, species, another_species):
    animal.species = species.id
    another_animal.species = species.id
    db.session.commit()
    resp = client.get('/species')
    expected_species = [
        {'id': species.id, 'name': species.name, 'animals': 2},
        {'id': another_species.id, 'name': another_species.name, 'animals': 0}
    ]
    assert resp.json == expected_species


def test_should_provide_empty_list_when_no_species_exist(client):
    resp = client.get('/species')
    assert [] == resp.json


def test_should_provide_species_details(client, animal, another_animal, species):
    animal.species = species.id
    another_animal.species = species.id
    db.session.commit()
    resp = client.get(f'/species/{species.id}')
    expected_response = {
        'id': species.id,
        'name': species.name,
        'description': species.description,
        'animals': [
            {
                'id': entry.id,
                'name': entry.name,
                'species': species.id
            }
            for entry in [animal, another_animal]
        ]
    }
    assert resp.json == expected_response


def test_should_not_provide_details_for_non_existing_species(client):
    resp = client.get('/species/9999')
    assert resp.status_code == 404
    assert resp.json == {'error': 'species does not exist'}
