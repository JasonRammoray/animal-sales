from sqlalchemy.orm import validates

from app import db
from app.models.animal_center import AnimalCenter
from app.models.species import Species


class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_id = db.Column(
        db.Integer,
        db.ForeignKey('animal_center.id', ondelete='CASCADE'),
        nullable=False
    )
    name = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(512), unique=False, nullable=False, default='')
    age = db.Column(db.Float, nullable=False)
    species = db.Column(
        db.Integer,
        db.ForeignKey('species.id', ondelete='CASCADE'),
        nullable=False
    )
    price = db.Column(db.Float, nullable=False, default=0)

    @validates('name')
    def validate_name(self, _, name):
        if not name:
            raise AssertionError('An animal must have name')

        l_len = len(name)
        if not 5 <= l_len <= 255:
            raise AssertionError('An animal name must be within 5 and 255 characters')
        return name

    @validates('age')
    def validate_age(self, _, age):
        if not age:
            raise AssertionError('An animal must have age')

        if age < 0 or age > 500:
            raise AssertionError('An animal age should be within 0 and 500 years')
        return age

    @validates('center_id')
    def validate_center_id(self, _, center_id):
        if not center_id:
            raise AssertionError('An animal must belong to a certain center')

        if AnimalCenter.query.get(center_id) is None:
            raise AssertionError(f'An animal could not be attached to a non-existing center {center_id}')
        return center_id

    @validates('species')
    def validate_species(self, _, species):
        if not species:
            raise AssertionError('An animal must belong to a certain species')

        if Species.query.get(species) is None:
            raise AssertionError(f'An animal could not be attached to a non-existing species {species}')
        return species

    @validates('price')
    def validate_price(self, _, price):
        if price < 0:
            raise AssertionError('An animal price should be greater or equal to zero')
        return price
