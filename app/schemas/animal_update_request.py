from app.schemas.animal_add_request import animal_add_payload_schema

animal_payload_add_props = animal_add_payload_schema['properties']

animal_update_payload_schema = {
    'type': 'object',
    'properties': animal_payload_add_props,
    'additionalProperties': False,
    'required': [],
    'anyOf': [
        {'required': [prop]} for prop in animal_payload_add_props.keys()
    ]
}
