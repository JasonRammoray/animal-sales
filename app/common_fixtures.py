import pytest
from flask.testing import FlaskClient

from app import create_app, db
from app.models.animal_center import AnimalCenter
from app.utils.jwt import generate_token


class CustomTestClient(FlaskClient):
    def open(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        return super().open(*args, **kwargs)


@pytest.fixture
def app_secret():
    return 'top secret'


@pytest.fixture
def client(app_secret, custom_config=None):
    default_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TOKEN_EXP_TIME': 1,
        'SECRET_KEY': app_secret
    }
    if custom_config:
        default_config.update(custom_config)
    app = create_app(default_config)
    app.test_client_class = CustomTestClient
    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
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
    yield animal_center
    AnimalCenter.query.filter_by(id=animal_center.id).delete()
    db.session.commit()


@pytest.fixture
def jwt_token(animal_center, app_secret):
    return generate_token(subject=animal_center.id, secret=app_secret, ttl=10)
