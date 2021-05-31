
from . import register
from core.context import Context
from core.graphics import Font


@register("bone")
def bone(map, trigger, entity, layer, x, y):
    context = Context.instance()
    sound_manger = Context.instance().sound_manager
    stack = context.data["stack"]
    world = context.data["world"]
    info = context.info
    font = Font()

    bone_item_id = 3

    def give_bone():
        stack.push_fitted(
            info.screen_width/2,
            info.screen_height/2,
            font,
            'Found key item: "Calcified bone"',
            wrap=400,
        )
        world.add_key(bone_item_id)
        sound = sound_manger.get_sound("key_item")
        sound.play()

    stack.push_fitted(
        info.screen_width/2,
        info.screen_height/2,
        font,
        "The skeleton collapsed into dust.",
        wrap=400,
        on_finish=give_bone
    )

    sound = sound_manger.get_sound("skeleton_destroy")
    sound.play()
    map.remove_trigger(73, 11, layer)
    map.remove_trigger(74, 11, layer)
    map.write_tile(74, 11, layer, 134, 0, True)
