import json
from combat import Dice


class StatModel:
    def __init__(self):
        with open("./defs/stat_def.json") as fp:
            self.data = json.load(fp)

    def __getitem__(self, key):
        return Dice(self.data[key]["dice"])

    def is_dice(self):
        pass
