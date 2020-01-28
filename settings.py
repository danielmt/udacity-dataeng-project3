from typing import Dict, Any

import configparser


CONFIG_FILE = "dwh.cfg"


def get_config() -> Dict[str, Any]:
    """returns dwh configuration (ini format)"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    return config
