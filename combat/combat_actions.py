from os import stat
from combat.combat_formula import HitResult, magic_attack
from core import Context
from combat.fx import CombatTextFX
from combat.fx import AnimEntityFX

# --------
# Registry
# --------
combat_action_registry = {}


def register_combat_action(name):
    def add_to_registry(func):
        combat_action_registry[name] = func
        return func
    return add_to_registry


# ----------------
# Helper Functions
# ----------------
def get_entity_effect(entity_effect_id):
    context = Context.instance()
    entity_defs = context.data["entity_definitions"]
    return entity_defs.get_entity_def(entity_effect_id)


def add_anim_effect(state, entity, offset_x, offset_y, anim_def, spf):
    state.add_effect(
        AnimEntityFX(
            entity.sprite.x + entity.width/2 + offset_x,
            entity.sprite.y + entity.height/2 + offset_y,
            anim_def,
            anim_def["frames"],
            spf
        )
    )


def add_text_number_effect(state, entity, number, color):
    state.add_effect(
        CombatTextFX(
            entity.sprite.x + entity.width/2,
            entity.sprite.y + entity.height/2,
            str(number),
            color
        )
    )


def stats_character_entity(state, actor):
    stats = actor.stats
    character = state.actor_char_map[actor]
    entity = character.entity
    return stats, character, entity


def give_revived_character_turn(character):
    pass


# -------
# Actions
# -------
@register_combat_action("hp_restore")
def hp_restore(state, owner, targets, item_def):
    restore_amount = item_def.get("restore", 255)
    anim_effect = get_entity_effect("fx_restore_hp")
    restore_color = (0, 255, 0, 255)

    for target in targets:
        stats, _, entity = stats_character_entity(state, target)
        max_hp = stats.get("hp_max")
        now_hp = stats.get("hp_now")

        if now_hp > 0:
            add_text_number_effect(
                state,
                entity,
                restore_amount,
                restore_color
            )
            now_hp = min(max_hp, now_hp + restore_amount)

        add_anim_effect(state, entity, 0, 0, anim_effect, 0.1)


@register_combat_action("mp_restore")
def mp_restore(state, owner, targets, item_def):
    restore_amount = item_def.get("restore", 50)
    anim_effect = get_entity_effect("fx_restore_mp")
    restore_color = (130, 200, 237, 255)

    for target in targets:
        stats, _, entity = stats_character_entity(state, target)
        max_mp = stats.get("mp_max")
        now_mp = stats.get("mp_now")
        now_hp = stats.get("hp_now")

        if now_hp > 0:
            add_text_number_effect(
                state,
                entity,
                restore_amount,
                restore_color
            )
            now_mp = min(max_mp, now_mp + restore_amount)
            stats.set("mp_now", now_mp)

        add_anim_effect(state, entity, 0, 0, anim_effect, 0.1)


@register_combat_action("revive")
def revive(state, owner, targets, item_def):
    restore_amount = item_def.get("restore", 100)
    anim_effect = get_entity_effect("fx_revive")
    restore_color = (0, 255, 0, 255)

    for target in targets:
        stats, character, entity = stats_character_entity(state, target)
        max_hp = stats.get("hp_max")
        now_hp = stats.get("hp_now")

        if now_hp == 0:
            now_hp = min(max_hp, now_hp + restore_amount)
            stats.set("hp_now", now_hp)
            add_text_number_effect(
                state,
                entity,
                restore_amount,
                restore_color
            )
            give_revived_character_turn(character)
        add_anim_effect(state, entity, 0, 0, anim_effect, 0.1)


@register_combat_action("elemental_spell")
def element_spell(state, owner, targets, spell_def):
    for target in targets:
        _, _, entity = stats_character_entity(state, target)
        demage, hit_result = magic_attack(state, owner, target, spell_def)

        if hit_result == HitResult.HIT:
            state.apply_demage(target, demage, False)

        element = spell_def.get("element")
        if element == "fire":
            add_anim_effect(
                state,
                entity,
                0,
                0,
                get_entity_effect("fx_fire"),
                0.06
            )
        if element == "electric":
            add_anim_effect(
                state,
                entity,
                0,
                0,
                get_entity_effect("fx_electric"),
                0.12
            )
        if element == "ice":
            add_anim_effect(
                state,
                entity,
                0,
                0,
                get_entity_effect("fx_ice_1"),
                0.1
            )
            add_anim_effect(
                state,
                entity,
                0,
                0,
                get_entity_effect("fx_ice_spark"),
                0.12
            )
            add_anim_effect(
                state,
                entity,
                entity.width * 0.8,
                0,
                get_entity_effect("fx_ice_2"),
                0.1
            )
            add_anim_effect(
                state,
                entity,
                entity.width * 0.8,
                -entity.height * 0.6,
                get_entity_effect("fx_ice_3"),
                0.1
            )
