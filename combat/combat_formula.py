def malee_attack(state, attacker, target):
    stats = attacker.stats
    enemy_stats = target.stats

    attack = stats.get("attack") + stats.get("strength")
    defence = enemy_stats.get("defence")
    demage = max(0, attack - defence)

    return demage
