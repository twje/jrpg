
from . import register
from model import PartyModel
from core.context import Context
from core.graphics import Font
from combat import Actor


@register("talk_recruit")
def talk_recruit(map, trigger, entity, layer, x, y):
    context = Context.instance()
    info = context.info
    stack = context.data["stack"]
    world = context.data["world"]
    npc = map.get_npc(x, y, layer)
    actor_def = PartyModel()[npc.actor_id]

    def on_recruit(index, item):
        world.party.add(Actor(actor_def))
        map.remove_npc(x, y, layer)

    stack.push_fitted(
        info.screen_width/2,
        info.screen_height/2,
        Font(),
        f"Recruit {actor_def['name']}?",
        wrap=400,
        choices={
            "options": [
                "Recruit",
                "Leave"
            ],
            "on_selection": on_recruit
        }
    )
