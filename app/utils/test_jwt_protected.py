from flask import current_app, g

from app.utils.jwt import generate_token
from app.utils.jwt_protected import jwt_protected


def test_should_forbid_access_without_credentials(client):
    @current_app.route('/test-route', methods=['POST'])
    @jwt_protected
    def test_route():
        return 'Only for the club members, pal'

    resp = client.post('/test-route')
    assert resp.status_code == 401


def test_should_restrict_access_for_fake_credentials(client, animal_center):
    @current_app.route('/test-route', methods=['POST'])
    @jwt_protected
    def test_route():
        return 'Fake news, witch hunt!'

    fake_token = generate_token(animal_center.id, secret='fake private key', ttl=3600)
    resp = client.post('/test-route', headers={'Authorization': f'Bearer {fake_token}'})
    assert resp.status_code == 401


def test_should_restrict_access_for_expired_credentials(client, animal_center, app_secret):
    @current_app.route('/test-route', methods=['POST'])
    @jwt_protected
    def test_route():
        return 'Sorry, mate, you are late'

    expired_token = generate_token(subject=animal_center.id, secret=app_secret, ttl=-1)
    resp = client.post('/test-route', headers={'Authorization': f'Bearer {expired_token}'})
    assert resp.status_code == 401


def test_should_grant_access_for_valid_credentials(client, jwt_token, animal_center):
    @current_app.route('/test-route', methods=['POST'])
    @jwt_protected
    def test_route():
        return 'Hello, authenticated user!'

    resp = client.post('/test-route', headers={'Authorization': f'Bearer {jwt_token}'})
    assert resp.status_code == 200
    assert g.entity_id == animal_center.id
