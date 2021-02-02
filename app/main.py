from app import create_app
from app.config import get_config

config = get_config()
app = create_app(config)
