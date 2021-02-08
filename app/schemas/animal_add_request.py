animal_add_payload_schema = {
    'type': 'object',
    'properties': {
        'centerId': {
            'type': 'number',
            'minimum': 1
        },
        'name': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 255
        },
        'description': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 512
        },
        'age': {
            'type': 'number',
            'minimum': 0,
            'maximum': 500
        },
        'species': {
            'type': 'number',
            'minimum': 1
        },
        'price': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1000000
        }
    },
    'additionalProperties': False,
    'required': ['centerId', 'name', 'age', 'species']
}
