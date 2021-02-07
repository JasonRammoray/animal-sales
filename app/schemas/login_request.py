from app.schemas.login_shard import login_shard
from app.schemas.password_shard import password_shard

login_request_schema = {
    'type': 'object',
    'properties': {
        'login': login_shard,
        'password': password_shard
    },
    'additionalProperties': False,
    'required': ['login', 'password']
}
