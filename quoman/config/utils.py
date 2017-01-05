import json
from os.path import join


def get_env(base_dir):
    """ Obtenemos las 'variables de entorno' desde un archivo json."""
    with open(join(base_dir, 'config/settings/settings.json')) as f:
        env = json.load(f)
        return env
