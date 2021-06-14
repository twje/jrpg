from core.graphics import TextureAtlas
from core.graphics import Sprite
import utils


class Icons:
    def __init__(self):
        self.texture_atalas = TextureAtlas.load_from_filepath(
            utils.lookup_texture_filepath("inventory_icons.png"),
            18,
            18
        )
        self.icon_defs = {
            "useable":  0,
            "accessory":  1,
            "weapon":  2,
            "sword":  3,
            "dagger":  4,
            "stave":  5,
            "armor":  6,
            "plate":  7,
            "leather":  8,
            "robe":  9,
            "uparrow":  10,
            "downarrow": 11
        }
        self.sprites = {}

        for key, value in self.icon_defs.items():
            self.sprites[key] = Sprite(self.texture_atalas[value])

    def try_get(self, index):
        return self.sprites.get(index)
