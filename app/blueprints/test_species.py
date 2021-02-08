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
