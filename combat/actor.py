import math
from .stats import Stat


def next_level(level):
    exponent = 1.5
    base_xp = 1000
    return math.floor(base_xp * math.pow(level, exponent))


class Actor:
    def __init__(self, actor_def):
        self.actor_def = actor_def
        self.stats = Stat(actor_def["stats"])
        self.stat_growth = actor_def["stat_growth"]
        self.xp = 0
        self.level = 1
        self.next_level_xp = next_level(self.level)

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
