from datetime import datetime, timedelta

import jwt


def generate_token(subject, secret, ttl):
    token_eol = datetime.utcnow() + timedelta(seconds=ttl)
    message = {
        'sub': subject,
        'exp': token_eol
    }
    return jwt.encode(message, secret, algorithm='HS256')
