login_request_schema = {
    'type': 'object',
    'properties': {
        'login': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 255
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 64
        }
    },
    'additionalProperties': False,
    'required': ['login', 'password']
}
