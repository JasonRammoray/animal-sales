from datetime import datetime, timedelta

import jwt


def generate_token(subject, secret, ttl):
    """
    Constructs a JWT token based on a provided subject,
    a secret key and a time to live in seconds
    :param subject: int an entity id that shall be encoded
    in a token
    :param secret: string a secret key that is being used
    to encode/decode a token
    :param ttl: int lifespan of a new token
    :return: string
    """
    token_eol = datetime.utcnow() + timedelta(seconds=ttl)
    message = {
        'sub': subject,
        'exp': token_eol
    }
    return jwt.encode(message, secret, algorithm='HS256')
