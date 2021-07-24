
from . import register
from core.context import Context
from core.graphics import Font


@register("crumble")
def crumble(map, trigger, entity, layer, x, y):
    context = Context.instance()
    sound_manger = Context.instance().sound_manager
    stack = context.data["stack"]
    info = context.info
    font = Font()

    def on_push(index, item):
        if index == 1:
            return
        stack.push_fitted(
            info.screen_width/2,
            info.screen_height/2,
            font,
            "The wall crumbles",
            wrap=400,
        )
        sound = sound_manger.get_sound("crumble")
        sound.play()

        map.remove_trigger(x, y, layer)
        map.write_tile(x, y, layer, 134, 0, False)

    # fix choices with Selection instance
    stack.push_fitted(
        info.screen_width/2,
        info.screen_height/2,
        font,
        "The wall here is crumbling. Push it?",
        wrap=400,
        choices={
            "options": [
                "Push the wall",
                "Leave it alone"
            ],
            "on_selection": on_push
        }
    )
