import random
from .oddmeant_table import OddmeantTable


class DropTable:
    def __init__(self, drop_def):
        self.xp = drop_def.get("xp", 0)
        self.gold = random.randint(drop_def["gold"][0], drop_def["gold"][1])
        self.always = drop_def.get("always", [])
        self.oddmeant_table = OddmeantTable(drop_def["chance"])

    def pick(self):
        return self.oddmeant_table.pick()
