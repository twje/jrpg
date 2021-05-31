
from . import register
from core.context import Context
from core.graphics import Font


@register("use_grate")
def use_grate(map, trigger, entity, layer, x, y):
    context = Context.instance()
    sound_manger = Context.instance().sound_manager
    world = context.data["world"]
    stack = context.data["stack"]
    info = context.info
    font = Font()
    bone_item_id = 3

    if not world.has_keyz(bone_item_id):
        return

    def on_open(index, item):
        if index == 1:
            return
        sound = sound_manger.get_sound("grate")
        sound.play()
        map.remove_trigger(x, y, layer)
        map.write_tile(57, 6, layer, 151,  is_collision=False)
        map.write_tile(58, 6, layer, 151,  is_collision=False)
        map.add_trigger(57, 6, layer, "grate_open")
        map.add_trigger(58, 6, layer, "grate_open")

    stack.push_fitted(
        info.screen_width/2,
        info.screen_height/2,
        font,
        "The wall here is crumbling. Push it?",
        wrap=400,
        choices={
            "options": [
                "Prize open the grate",
                "Leave it alone"
            ],
            "on_selection": on_open
        }
    )
