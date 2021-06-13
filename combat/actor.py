"""
monsters as well as party members
"""

import math
from core import Context
from core.graphics import SpriteFont
from item_db import items_db
from .stats import Stat
from core.graphics import Sprite
import utils


def next_level(level):
    exponent = 1.5
    base_xp = 1000
    return math.floor(base_xp * math.pow(level, exponent))


class Actor:
    # labels
    EQUIP_SLOT_LABELS = [
        "Weapon:",
        "Armor:",
        "Accessory:",
        "Accessory:"
    ]
    EQUIP_SLOT_ID = [
        "weapon",
        "armor",
        "acces1",
        "acces2",
    ]
    ACTOR_STATS = [
        "str",
        "spd",
        "int",
    ]
    ITEM_STATS = [
        "attack",
        "defense",
        "magic",
        "resist",
    ]
    ACTOR_STAT_LABELS = [
        "Strength",
        "Speed",
        "Intelligence",
    ]
    ITEM_STAT_LABELS = [
        "Attack",
        "Defense",
        "Magic",
        "Resist",
    ]
    ACTION_LABELS = {
        "attack": "Attack",
        "item": "Item",
    }

    def __init__(self, party_model):
        self.context = Context.instance()
        self.world = self.context.data["world"]
        self.party_model = party_model
        self.name = party_model["name"]
        self.id = party_model["id"]
        self.stats = Stat(party_model["stats"])
        self.stat_growth = party_model["stat_growth"]
        self.actions = party_model["actions"]
        self.xp = 0
        self.level = 1
        self.next_level_xp = next_level(self.level)
        self.equipment = {
            "weapon": party_model.get("weapon"),
            "armor": party_model.get("armor"),
            "acces1": party_model.get("acces1"),
            "acces2": party_model.get("acces2"),
        }
        self.active_equip_slots = party_model.get("equip_slots", [0, 1, 2])

        if "portrait" in self.party_model:
            self.portrait = Sprite.load_from_filesystem(
                utils.lookup_texture_filepath(self.party_model["portrait"])
            )

    def equip(self, slot, item):
        raise NotImplementedError

    def ready_to_level_up(self):
        return self.xp >= self.next_level_xp

    def add_xp(self, xp):
        self.xp += xp
        return self.ready_to_level_up()

    def create_level_up(self):
        levelup = {
            "xp": -self.next_level_xp,
            "level": 1,
            "stats": {}
        }

        for key, dice in self.stat_growth.items():
            levelup["stats"][key] = dice.roll()

        return levelup

    def apply_level(self, levelup):
        self.xp += levelup["xp"]
        self.level += levelup["level"]
        self.next_level_xp = next_level(self.level)

        assert self.xp >= 0

        for key, value in levelup["stats"].items():
            base_stat = self.stats.get_base(key)
            self.stats.set_base(key, base_stat + value)

    def render_equipment(self, renderer, font, scale, x, y, index):
        x = x
        label = self.EQUIP_SLOT_LABELS[index]
        lable_sprite = SpriteFont(label)
        lable_sprite.set_position(x, y)
        renderer.draw(lable_sprite)

        slot_id = self.EQUIP_SLOT_ID[index]
        text = "none"
        if self.equipment[slot_id] is not None:
            item_id = self.equipment[slot_id]
            item = items_db[item_id]
            text = item["name"]

        text_sprite = SpriteFont(text)
        text_sprite.set_position(x + lable_sprite.width + 5, y)
        renderer.draw(text_sprite)
