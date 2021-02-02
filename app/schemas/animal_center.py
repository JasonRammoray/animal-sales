animal_center_payload_schema = {
    'type': 'object',
    'properties': {
        'login': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'address': {
            'type': 'string'
        }
    },
    'required': ['login', 'password', 'address']
}
