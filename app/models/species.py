from sqlalchemy.orm import validates

from app import db


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(512), unique=False, nullable=False)
    price = db.Column(db.Float, default=0)

    @validates('name')
    def validate_login(self, _, name):
        if not name:
            raise AssertionError('A species must have name')

        l_len = len(name)
        if not 5 <= l_len <= 255:
            raise AssertionError('A species name must be within 5 and 255 characters')
        return name

    @validates('description')
    def validate_login(self, _, description):
        if not description:
            raise AssertionError('A species must have description')

        l_len = len(description)
        if not 5 <= l_len <= 255:
            raise AssertionError('A species description must be within 5 and 255 characters')
        return description

    @validates('price')
    def validate_login(self, _, price):
        if price < 0:
            raise AssertionError('A species price should be positive')

        if price >= 1e9:
            raise AssertionError('A species can not cost more than a billion')
        return price
