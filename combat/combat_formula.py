from enum import Enum
import random
import math
from utils import clamp, strip_filepath


class HitResult(Enum):
    MISS = 0
    DODGE = 1
    HIT = 2
    CRITICAL = 3


def can_flee(state, fleer):
    flee_chance = 0.35
    speed = fleer.stats.get("speed")

    enemy_count = 0
    total_speed = 0
    for enemy_actor in state.actors["enemy"]:
        speed = enemy_actor.stats.get("speed")
        total_speed = total_speed + speed
        enemy_count += 1

    avg_speed = total_speed/enemy_count

    if speed > avg_speed:
        flee_chance += 0.15
    else:
        flee_chance -= 0.15

    return random.uniform(0, 1) <= flee_chance


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


def is_hit_magic(state, attacker, target, spell_def):
    hit_chance = spell_def["base_hit_chance"]
    if random.uniform(0, 1) <= hit_chance:
        return HitResult.HIT
    else:
        return HitResult.MISS


def calc_base_spell_demage(spell_def):
    base = spell_def["base_demage"]
    if isinstance(base, list):
        base = random.uniform(base[0], base[1])
    demage = base * 4

    return demage


def calc_spell_caster_bonus(base, attacker):
    level = attacker.level
    stats = attacker.stats
    bonus = level * stats.get("intelligence") * (base/32)

    return bonus


def calc_target_elemental_modifier(spell_def, target):
    element = spell_def.get("element")
    if element is not None:
        modifier = target.stats.get(element)
        return 1 + modifier  # 1 is no modifier applied
    return 0


def calc_target_resistance_modifier(target):
    resist = min(255, target.stats.get("resist"))
    resist = 1 - (resist / 255)
    return resist


def calc_spell_def_demage(state, attacker, target, spell_def):
    demage = calc_base_spell_demage(spell_def)
    demage += calc_spell_caster_bonus(demage, attacker)
    demage *= calc_target_elemental_modifier(spell_def, target)
    demage *= calc_target_resistance_modifier(target)

    return math.floor(demage)


def magic_attack(state, attacker, target, spell_def):
    demage = 0
    hit_result = is_hit_magic(state, attacker, target, spell_def)

    if hit_result == HitResult.MISS:
        return math.floor(demage), HitResult.Miss

    demage = calc_spell_def_demage(state, attacker, target, spell_def)

    return math.floor(demage), HitResult.HIT


def steal(attacker, target):
    cts = 0.05
    if attacker.level > target.level:
        cts = (50 + attacker.level - target.level)/128
        cts = clamp(cts, 0.05, 0.95)

    rand = random.uniform(0, 1)
    return rand <= cts
