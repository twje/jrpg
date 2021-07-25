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
        party_member["stat_growth"]["hp_max"] = Dice(
            party_member["stat_growth"]["hp_max"]["dice"])
        party_member["stat_growth"]["mp_max"] = Dice(
            party_member["stat_growth"]["mp_max"]["dice"])
        party_member["stat_growth"]["strength"] = self.stat_model[party_member["stat_growth"]["strength"]]
        party_member["stat_growth"]["speed"] = self.stat_model[party_member["stat_growth"]["speed"]]
        party_member["stat_growth"]["intelligence"] = self.stat_model[party_member["stat_growth"]["intelligence"]]

        return party_member
