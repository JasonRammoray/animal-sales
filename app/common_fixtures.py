import flask
import pytest

from app import create_app, db


@pytest.fixture
def some():
    return 2


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
            test_client.headers = {
                'Content-Type': 'application/json'
            }
            yield test_client
        db.session.remove()
        db.drop_all()
