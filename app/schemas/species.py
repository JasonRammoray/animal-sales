species_payload_schema = {
    'type': 'object',
    'properties': {
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
        'price': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1000000000
        }
    },
    'additionalProperties': False,
    'required': ['name', 'description', 'price']
}
