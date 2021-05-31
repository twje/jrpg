
from dataclasses import dataclass
from . import register
from core.context import Context
from core.graphics import Font
from core.graphics import formatter


@dataclass
class Bounds:
    x: int
    y: int
    width: int
    height: int


@register("talk_gregor")
def talk_gregor(map, trigger, entity, layer, x, y):
    context = Context.instance()
    stack = context.data["stack"]
    info = context.info

    gregor = map.npc_by_id["gregor"]
    if gregor.entity.tile_x == x and gregor.entity.tile_y == y - 1:
        speach = [
            "You're another black blood aren't you?",
            "Come the morning, they'll kill you, just like the others.",
            "If I was you, I'd try and escape.",
            "Pry the drain open, with that big bone you're holding."
        ]

        textbox_bounds = Bounds(0, 0, 500, 102)
        stack.push_fixed(
            formatter.center_x(info, textbox_bounds),
            formatter.bottom_justify(0, info, textbox_bounds),
            textbox_bounds.width,
            textbox_bounds.height,
            Font(),
            speach[gregor.talk_index],
            title="Prisoner: "
        )
        gregor.talk_index = (gregor.talk_index + 1) % len(speach)
