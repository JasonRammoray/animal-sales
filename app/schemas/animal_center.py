from app.schemas.login_shard import login_shard
from app.schemas.password_shard import password_shard

animal_center_payload_schema = {
    'type': 'object',
    'properties': {
        'login': login_shard,
        'password': password_shard,
        'address': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 255
        }
    },
    'additionalProperties': False,
    'required': ['login', 'password', 'address']
}
