import configparser


CONFIG_FILE = "dwh.cfg"


def get_config() -> configparser.ConfigParser:
    """returns dwh configuration (ini format)"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    return config
