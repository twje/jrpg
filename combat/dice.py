from dataclasses import dataclass
import random


@dataclass
class Die:
    rolls: int
    sides: int
    modifier: int


class Dice:
    def __init__(self, dice_str):
        self.dice = []
        self.parse(dice_str)

    def parse(self, dice_str):
        index = 0

        while(index < len(dice_str)):
            die, index = self.parse_die(dice_str, index)
            self.dice.append(die)
            index += 1  # eat ' '

    def parse_die(self, dice_str, index):
        rolls, index = self.parse_number(dice_str, index)
        index += 1  # move past the 'D'

        sides, index = self.parse_number(dice_str, index)
        if index == len(dice_str) or dice_str[index] == ' ':
            return Die(rolls, sides, 0), index

        if dice_str[index] == '+':
            index += 1  # move past the '+'
            plus, index = self.parse_number(dice_str, index)
            return Die(rolls, sides, plus), index

    def parse_number(self, dice_str, index):
        sub_str = ""
        length = len(dice_str)
        for i in range(index, length):
            if not dice_str[i].isdigit():
                return int(sub_str), i
            sub_str += dice_str[i]

        return int(sub_str), length

    def role_die(self, rolls, faces, modifier):
        total = 0
        for _ in range(0, rolls):
            total += random.randint(1, faces)
        return total + modifier

    def roll(self):
        total = 0
        for die in self.dice:
            total += self.role_die(die.rolls, die.sides, die.modifier)
        return total


dice = Dice("1D6 1D6+8")
