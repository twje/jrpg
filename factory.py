import json
from entity_defs import EntityDefs
from manifest import Manifest


def load_manifest():
    with open("config/manifest.json", "r") as fp:
        return Manifest(json.load(fp))


def load_entity_definition():
    with open("defs/entity_defs.json", "r") as fp:
        return EntityDefs(json.load(fp))


def load_enemy_definition():
    with open("defs/enemy_defs.json", "r") as fp:
        return json.load(fp)

def load_application_settings():
    with open("config/settings.json", "r") as fp:
        return json.load(fp)
