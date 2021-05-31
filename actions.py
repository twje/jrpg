from scripts import script_registry
from character import Character
import utils

action_registry = {}


def register_action(name):
    """add resolver class to registry"""
    def add_func(func):

        action_registry[name] = func
        return func

    return add_func


@register_action("Teleport")
def teleport(map, tile_x, tile_y):
    def action(trigger, entity):
        entity.set_tile_pos(
            tile_x,
            tile_y,
            entity.layer,
            map
        )

    return action


@register_action("AddNPC")
def add_npc(map, definition, npc_id):
    def action(trigger, entity, layer, tile_x, tile_y):
        character = Character.create_from_id(definition, map)

        # defaults to character attribute
        character.entity.set_tile_pos(
            utils.ternary_not(tile_x, character.entity.tile_x),
            utils.ternary_not(tile_y, character.entity.tile_y),
            utils.ternary_not(layer, character.entity.layer),
            map=map)
        map.add_npc(character)
        assert npc_id not in map.npc_by_id
        character.id = npc_id
        map.npc_by_id[npc_id] = character

    return action


@register_action("RunScript")
def run_script(map, func):
    def action(trigger, entity, layer, tile_x, tile_y):
        script_registry[func](map, trigger, entity, layer, tile_x, tile_y)
    return action
