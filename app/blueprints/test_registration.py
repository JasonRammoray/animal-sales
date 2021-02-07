def test_should_create__center(client, secure_password):
    center_address = 'test address'
    resp = client.post('/register', json={
        'login': 'test_animal_center',
        'password': secure_password,
        'address': center_address
    })
    assert resp.json == {'address': center_address, 'id': 1}


def test_should_not_create_center_without_password(client):
    resp = client.post('/register', json={
        'login': 'test_animal_center',
        'address': 'test address'
    })
    assert resp.status_code == 400
    assert "'password' is a required " in resp.json['error']


def test_should_not_create_center_with_weak_password(client):
    resp = client.post('/register', json={
        'login': 'test_animal_center',
        'password': 'qwerty123',
        'address': 'test address'
    })
    assert resp.status_code == 400
    assert resp.json == {'error': 'A center password must be between 8 and 64 characters and contain at least one '
                                  'digit, one special character, and one uppercase letter'}


def test_should_not_create_center_without_address(client, secure_password):
    resp = client.post('/register', json={
        'login': 'test_animal_center',
        'password': secure_password
    })
    assert resp.status_code == 400
    assert "'address' is a required " in resp.json['error']


def test_should_not_create_center_with_lengthy_address(client, secure_password):
    resp = client.post('/register', json={
        'login': 'test_animal_center',
        'password': secure_password,
        'address': 'test address' * 100
    })
    assert resp.status_code == 400


def test_should_not_create_center_with_non_unique_login(client, secure_password):
    address = 'test address'
    login = 'x_lab'
    client.post('/register', json={
        'login': login,
        'password': secure_password,
        'address': address
    })
    resp = client.post('/register', json={
        'login': login,
        'password': secure_password,
        'address': address
    })
    assert resp.status_code == 400
    assert resp.json == {'error': 'login is occupied'}
