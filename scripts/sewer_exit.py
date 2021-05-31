
from . import register
from core.context import Context
from state_stack.world import GameOverState


@register("sewer_exit")
def sewer_exit(map, trigger, entity, layer, x, y):
    context = Context.instance()
    stack = context.data["stack"]
    stack.pop()
    stack.push(GameOverState())
