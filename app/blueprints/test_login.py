import re

from app.models.api_access_request import ApiAccessRequest


def test_should_issue_token_for_valid_credentials(client, animal_center, secure_password):
    resp = client.post('/login', json={
        'login': animal_center.login,
        'password': secure_password
    })
    token = resp.json.get('token', '')
    assert re.match('^[a-zA-Z\\d]+\\.[a-zA-Z\\d]+\\.[a-zA-Z\\d_-]+$', token) is not None


def test_should_not_issue_token_for_non_existing_center(client, secure_password):
    resp = client.post('/login', json={
        'login': 'cyber animals center',
        'password': secure_password
    })
    assert resp.status_code == 401
    assert resp.json['error'] == 'invalid credentials'


def test_should_not_issue_token_for_existing_center_with_invalid_password(client, animal_center):
    resp = client.post('/login', json={
        'login': animal_center.login,
        'password': 'we@do$forget#p2ssWords'
    })
    assert resp.status_code == 401
    assert resp.json['error'] == 'invalid credentials'


def test_should_not_issue_token_for_invalid_request_payload(client):
    resp = client.post('/login', json={
        'login': 'gimme your token now, it is not a scam',
    })
    assert resp.status_code == 400


def test_should_memorize_successful_token_request(client, animal_center, secure_password):
    assert len(ApiAccessRequest.query.all()) == 0
    client.post('/login', json={
        'login': animal_center.login,
        'password': secure_password
    })
    api_requests = ApiAccessRequest.query.all()
    assert len(api_requests) == 1
    assert api_requests[0].center_id == animal_center.id
