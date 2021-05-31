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
            "useable": 0,
            "accessory": 1,
            "weapon": 2,
            "armor": 3,
            "uparrow": 4,
            "downarrow": 5,
        }
        self.sprites = {}

        for key, value in self.icon_defs.items():
            self.sprites[key] = Sprite(self.texture_atalas[value])

    def try_get(self, index):
        return self.sprites.get(index)
