from .dice import Dice
from .stats import StatID
#from .actor import Actor

"""
stats = {
    StatID.HP_NOW: 300,
    StatID.HP_MAX: 300,
    StatID.MP_NOW: 300,
    StatID.MP_MAX: 300,
    StatID.STRENGTH: 10,
    StatID.SPEED: 10,
    StatID.INTELLIGENCE: 10,
}

growth = {
    "fast": Dice("3d2"),
    "med": Dice("1d3"),
    "slow": Dice("1d2")
}

hero_def = {
    "stats": stats,
    "stat_growth": {
        StatID.HP_MAX: Dice("4d50+100"),
        StatID.MP_MAX: Dice("2d50+100"),
        StatID.STRENGTH: growth["fast"],
        StatID.SPEED: growth["fast"],
        StatID.INTELLIGENCE: growth["med"],
    }
}

thief_def = {
    "stats": stats,
    "stat_growth": {
        StatID.HP_MAX: Dice("4d40+100"),
        StatID.MP_MAX: Dice("2d25+100"),
        StatID.STRENGTH: growth["fast"],
        StatID.SPEED: growth["fast"],
        StatID.INTELLIGENCE: growth["slow"],
    }
}


mage_def = {
    "stats": stats,
    "stat_growth": {
        StatID.HP_MAX: Dice("3d40+100"),
        StatID.MP_MAX: Dice("4d50+100"),
        StatID.STRENGTH: growth["med"],
        StatID.SPEED: growth["med"],
        StatID.INTELLIGENCE: growth["fast"],
    }
}

mage = Actor(mage_def)
thief = Actor(thief_def)
hero = Actor(hero_def)


def print_level_up(level_up):
    print(level_up)


def apply_xp(actor, xp):
    actor.add_xp(xp)

    while actor.ready_to_level_up():
        level_up = actor.create_level_up()
        level_number = actor.level + level_up["level"]
        print(f"Level Up! {level_number}")
        print_level_up(level_up)
        actor.apply_level(level_up)        

hero = Actor(hero_def)
apply_xp(hero, 10001)
"""

from combat.combat_scene import CombatScene

from dataclasses import dataclass

@dataclass
class TestActor:
    name: str
    speed: int
    attack: int
    HP: int
    _is_player: bool

    def is_player(self):
        return self._is_player

    def is_koed(self):
        return self.HP <= 0

    def ko(self):
        self.HP = 0
    
print("--start--")

party = [TestActor("hero", 3, 2, 5, True)]
enemies = [TestActor("goblin", 2, 2, 5, False)]
scene = CombatScene(party, enemies)

turns = 36
for _ in range(turns):
    scene.update()

