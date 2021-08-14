from enum import Enum
import random
import math
from utils import clamp


class HitResult(Enum):
    MISS = 0
    DODGE = 1
    HIT = 2
    CRITICAL = 3


def malee_attack(state, attacker, target):
    demage = 0
    hit_result = is_hit(state, attacker, target)

    if hit_result == HitResult.MISS:
        return math.floor(demage), HitResult.MISS

    if is_dodged(state, attacker, target):
        return math.floor(demage), HitResult.DODGE

    demage = calc_demage(state, attacker, target)

    if hit_result == HitResult.HIT:
        return math.floor(demage), HitResult.HIT

    # critical
    assert hit_result == HitResult.CRITICAL

    demage += base_attack(state, attacker, target)
    return math.floor(demage), HitResult.CRITICAL


def is_hit(state, attacker, target):
    stats = attacker.stats
    speed = stats.get("speed")
    intelligence = stats.get("intelligence")

    cth = 0.7  # chance to hit
    ctc = 0.1  # chance to crit

    bonus = ((speed + intelligence) / 2) / 255
    cth = cth + (bonus / 2)

    rand = random.uniform(0, 1)
    is_hit = rand <= cth
    is_crit = rand <= ctc

    if is_crit:
        return HitResult.CRITICAL
    elif is_hit:
        return HitResult.HIT
    else:
        return HitResult.MISS


def is_dodged(state, attacker, target):
    stats = attacker.stats
    enemy_stats = target.stats

    speed = stats.get("speed")
    enemy_speed = enemy_stats.get("speed")

    ctd = 0.03
    speed_diff = speed - enemy_speed

    # clamp speed diff to plus or minus 10%
    speed_diff = clamp(speed_diff, -10, 10) * 0.01

    ctd = max(0, ctd + speed_diff)

    return random.uniform(0, 1) <= ctd


def is_countered(state, attacker, target):    
    counter = target.stats.get("counter")
    return random.uniform(0, 1) < counter


def base_attack(state, attacker, target):
    stats = attacker.stats
    strength = stats.get("strength")
    attack_stat = stats.get("attack")

    attack = int((strength / 2) + attack_stat)

    return random.randint(attack, attack * 2)


def calc_demage(state, attacker, target):
    target_stats = target.stats
    defence = target_stats.get("defence")

    attack = base_attack(state, attacker, target)

    return math.floor(max(0, attack - defence))
