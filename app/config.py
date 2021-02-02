import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.getcwd(), 'config.ini')
    config.read(config_path)
    return config
