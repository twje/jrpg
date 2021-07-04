from scripts import script_registry
from character import Character
from model import PartyModel
from core.context import Context
from core.graphics import Font
from item_db import items_db
from combat import Actor
from entity import Entity
from trigger import Trigger
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


@register_action("RemoveNPC")
def remove_npc(map, npc_id):
    def action(trigger, entity, layer, tile_x, tile_y):
        npc = map.npc_by_id[npc_id].entity
        assert npc is not None
        map.remove_npc(npc.tile_x, npc.tile_y, npc.layer)
    return action


@register_action("AddPartyMember")
def add_party_member(actor_id):
    def action(trigger, entity, layer, tile_x, tile_y):
        context = Context.instance()
        world = context.data["world"]
        actor_def = PartyModel()[actor_id]
        world.party.add(Actor(actor_def))
    return action


@register_action("AddChest")
def add_chest(map, entity_id, loot, chest_x, chest_y, chest_layer=0):
    def action(trigger, entity, layer, tile_x, tile_y):
        context = Context.instance()        
        entity_defs = context.data["entity_definitions"]        
        entity_def = entity_defs.get_entity_def(entity_id)
        chest = Entity(entity_def)
        chest.set_tile_pos(chest_x, chest_y, chest_layer, map)

        def on_open_chest(*args):    
            stack = context.data["stack"]
            world = context.data["world"]
            info = context.info
            if loot is None:                    
                stack.push_fitted(
                    info.screen_width/2,
                    info.screen_height/2,
                    Font(),
                    "The chest is empty!",
                    wrap=400,
                )
            else:
                world.add_loot(loot)
                for item in loot:
                    count = item.get("count", 1)
                    name = items_db[item["id"]]["name"]
                    message = f"Got {name}"
                    if count > 1:
                        message += f" x{count}"
                    stack.push_fitted(
                        info.screen_width/2,
                        info.screen_height/2,
                        Font(),
                        message,
                        wrap=400,
                    )

            map.remove_trigger(chest.tile_x, chest.tile_y, chest.layer)
            chest.set_frame(entity_def["open_frame"])

        trigger = Trigger({ "on_use": on_open_chest })
        map.add_full_trigger(trigger, chest.tile_x, chest.tile_y, chest.layer)

    return action
