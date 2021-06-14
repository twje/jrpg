
from . import register
from model import PartyModel
from core.context import Context
from core.graphics import Font


@register("talk_recruit")
def talk_recruit(map, trigger, entity, layer, x, y):
    from storyboard.storyboard import Storyboard
    from storyboard import events

    context = Context.instance()
    info = context.info
    stack = context.data["stack"]
    npc = map.get_npc(x, y, layer)
    actor_def = PartyModel()[npc.actor_id]

    def on_recruit(index, item):
        if item == "Recruit":
            fadeout = [
                events.fade_out_char("handin", npc.id),
                events.run_action(
                    "RemoveNPC",
                    {
                        "map": "handin",
                        "npc_id": npc.id
                    },
                    {
                        "map": events.get_map_ref
                    }
                ),
                events.run_action(
                    "AddPartyMember",
                    {
                        "actor_id": npc.id
                    }
                ),
                events.hand_off("handin")
            ]
            map.remove_trigger(x, y, layer)
            storboard = Storyboard(stack, fadeout, True)
            stack.push(storboard)

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
