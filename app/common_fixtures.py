import pytest
from flask.testing import FlaskClient

from app import create_app, db
from app.models.animal_center import AnimalCenter
from app.models.animals import Animals
from app.models.species import Species
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
    animal_center = AnimalCenter(login='test_center_123', address='test address')
    animal_center.set_password(secure_password)
    db.session.add(animal_center)
    db.session.commit()
    yield animal_center


@pytest.fixture
def another_animal_center(secure_password):
    another_animal_center = AnimalCenter(login='test_center_456', address='test land, test street')
    another_animal_center.set_password(secure_password[::-1])
    db.session.add(another_animal_center)
    db.session.commit()
    yield another_animal_center


@pytest.fixture
def species():
    new_species = Species(
        name='test animal species',
        description='This is a lovely test animal species',
        price=999.5
    )
    db.session.add(new_species)
    db.session.commit()
    yield new_species


@pytest.fixture
def another_species():
    another_new_species = Species(
        name='yet another test animal species',
        description='This is an alternative test species',
        price=134.98
    )
    db.session.add(another_new_species)
    db.session.commit()
    yield another_new_species


@pytest.fixture
def animal(species, animal_center):
    animal = Animals(
        name='test animal',
        description='the most cute animal in the test world',
        center_id=animal_center.id,
        species=species.id,
        age=4,
        price=42.5
    )
    db.session.add(animal)
    db.session.commit()
    yield animal


@pytest.fixture
def another_animal(another_species, another_animal_center):
    another_animal = Animals(
        name='test animal 2',
        description='the second most cute animal in the test world',
        center_id=another_animal_center.id,
        species=another_species.id,
        age=14,
        price=24.8
    )
    db.session.add(another_animal)
    db.session.commit()
    yield another_animal


@pytest.fixture
def jwt_token(animal_center, app_secret):
    return generate_token(subject=animal_center.id, secret=app_secret, ttl=10)


@pytest.fixture
def auth_http_headers(jwt_token):
    return {'Authorization': f'Bearer {jwt_token}'}
