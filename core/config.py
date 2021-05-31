from core import dirs
import json


def load_settings():
    with open(dirs.JSON_SETTINGS) as fp:
        return json.load(fp)


def load_manifest():
    with open(dirs.JSON_MANIFEST) as fp:
        return json.load(fp)
