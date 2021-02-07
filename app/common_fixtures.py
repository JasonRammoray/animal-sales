import flask
import pytest

from app import create_app, db
from app.models.animal_center import AnimalCenter


@pytest.fixture
def some():
    return 2


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TOKEN_EXP_TIME': 1,
        'SECRET_KEY': 'super secret'
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


@pytest.fixture
def secure_password():
    return 'S@cure#pass!Word42'


@pytest.fixture
def animal_center(secure_password):
    login = 'test_center_123'
    animal_center = AnimalCenter(login=login, address='test address')
    animal_center.set_password(secure_password)
    db.session.add(animal_center)
    db.session.commit()
    return animal_center
