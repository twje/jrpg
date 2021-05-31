
from . import register
from core.context import Context


@register("move_gregor")
def move_gregor(map, trigger, entity, layer, x, y):
    context = Context.instance()
    world = context.data["world"]
    gregor = map.npc_by_id["gregor"]

    bone_item_id = 3
    if world.has_keyz(bone_item_id):
        gregor.follow_path([
            "up",
            "up",
            "up",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "down",
            "down",
            "down",
        ])
        map.remove_trigger(x, y, layer)
