import secrets

from app import create_app
from app.config import get_config

parsed_config = get_config()
app_config = {
    'SQLALCHEMY_DATABASE_URI': parsed_config.get('DATABASE', 'uri', fallback='sqlite:///animal_sales.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': parsed_config.getboolean('DATABASE', 'track_modifications', fallback=False),
    'AUDIT_LOG': parsed_config.get('LOGGING', 'audit_log'),
    'TOKEN_EXP_TIME': parsed_config.getint('TOKEN', 'expiration_time', fallback=24),
    'SECRET_KEY': parsed_config.get('COMMON', 'secret_key', fallback=secrets.token_hex(64))
}
app = create_app(app_config)
