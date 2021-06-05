import json
from .stat_model import StatModel
from combat import Dice
import copy

class PartyModel:
    def __init__(self):
        self.stat_model = StatModel()
        with open("./defs/party_def.json") as fp:
            self.data = json.load(fp)

    def __getitem__(self, key):
        party_member = copy.deepcopy(self.data[key])
        party_member["stat_growth"]["hp_max"] = Dice(party_member["stat_growth"]["hp_max"]["dice"])
        party_member["stat_growth"]["mp_max"] = Dice(party_member["stat_growth"]["mp_max"]["dice"])
        party_member["stat_growth"]["str"] = self.stat_model[party_member["stat_growth"]["str"]]
        party_member["stat_growth"]["spd"] = self.stat_model[party_member["stat_growth"]["spd"]]
        party_member["stat_growth"]["int"] = self.stat_model[party_member["stat_growth"]["int"]]

        return party_member
    