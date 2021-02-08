import functools

import jwt
from flask import request, current_app, abort, make_response, jsonify, g
from jwt import DecodeError, ExpiredSignatureError

from app.models.animal_center import AnimalCenter


class CenterLookupError(Exception):
    pass


def jwt_protected(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.strip().replace('Bearer ', '')
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            entity_id = payload.get('sub')
            if AnimalCenter.query.get(entity_id) is None:
                raise CenterLookupError(f'Claimed center {entity_id} does not exist')
            g.entity_id = entity_id
        except (DecodeError, ExpiredSignatureError, CenterLookupError):
            abort(make_response(jsonify({'error': 'invalid auth credentials'}), 401))
        return fn(*args, **kwargs)
    return wrapper
