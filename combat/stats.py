import copy


class StatID:
    HP_NOW = "hp_now"
    HP_MAX = "hp_max"
    MP_NOW = "mp_now"
    MP_MAX = "mp_max"
    STRENGTH = "str"
    SPEED = "spd"
    INTELLIGENCE = "int"


class StatModifier:
    def __init__(self, modifier):
        self.add = modifier.get("add", {})
        self.mult = modifier.get("mult", {})

    def get_add(self, stat_id):        
        return self.add.get(stat_id, 0)

    def get_mult(self, stat_id):
        return self.mult.get(stat_id, 0)


class Stat:
    def __init__(self, stats):
        self.base = copy.copy(stats)
        self.modifiers = {}

    def get_base(self, stat_id):
        return self.base.get(stat_id, 0)

    def set_base(self, stat_id, value):
        self.base[stat_id] = value

    def add_modifier(self, modifier_id, modifier):
        self.modifiers[modifier_id] = StatModifier(modifier)

    def remove_modifier(self, modifier_id):
        del self.modifiers[modifier_id]

    def get(self, stat_id):
        total = self.get_base(stat_id)
        multiplier = 0

        for modifier in self.modifiers.values():
            total += modifier.get_add(stat_id)
            multiplier += modifier.get_mult(stat_id)

        return total + (total * multiplier)
