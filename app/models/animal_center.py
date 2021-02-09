import re

from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

VALID_PASSWORD_RE = '(?=.*[A-Z])(?=.*\\d)(?=.*[%@_#^])^.{8,64}$'


class AnimalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=False)
    api_requests = db.relationship(
        'ApiAccessRequest',
        cascade='all,delete,delete-orphan',
        backref='center'
    )
    animals = db.relationship(
        'Animals',
        cascade='all,delete,delete-orphan',
        backref='center',
        lazy=True
    )

    @validates('login')
    def validate_login(self, _, login):
        if not login:
            raise AssertionError('A center login has not been provided')

        l_len = len(login)
        if not 5 <= l_len <= 255:
            raise AssertionError('A center login len must be within 5 and 255 characters')
        return login

    @validates('address')
    def validate_address(self, _, address):
        if not address:
            raise AssertionError('A center address has not been provided')

        a_len = len(address)
        if not 5 <= a_len <= 255:
            raise AssertionError('A center address len must be within 5 and 255 characters')
        return address

    @staticmethod
    def get_password_hash(password):
        return generate_password_hash(password)

    def set_password(self, password):
        if not password:
            raise AssertionError('A center password has not been provided')

        if re.match(VALID_PASSWORD_RE, password) is None:
            raise AssertionError(
                """A center password must be between 8 and 64 characters and contain at least one digit,"""
                """ one special character, and one uppercase letter"""
            )
        self.password_hash = self.get_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Animal center {self.login} at {self.address}'
