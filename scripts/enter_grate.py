from core.context import Context
from . import register


@register("enter_grate")
def enter_grate(map, trigger, entity, layer, x, y):
    from storyboard.storyboard import Storyboard
    from storyboard import events

    context = Context.instance()
    sound_manger = context.sound_manager
    stack = context.data["stack"]

    sound = sound_manger.get_sound("reveal")
    sound.play()

    map.remove_trigger(57, 6, 0)
    map.remove_trigger(58, 6, 0)

    cutscene = [
        events.black_screen("blackscreen", 0),
        events.no_block(
            events.fade_out_char("handin", "hero")
        ),
        events.run_action(
            "AddNPC",
            {
                "map": "handin",
                "definition": "guard",
                "npc_id": "guard1",
                "tile_x": 35,
                "tile_y": 20,
            },
            {
                "map": events.get_map_ref
            }
        ),
        events.wait(2),
        events.no_block(
            events.move_npc("gregor", "handin", [
                "up",
                "up",
                "up",
                "up",
                "left",
                "left",
                "left",
                "left",
                "left",
                "left",
                "down",
                "down"
            ]),
        ),
        events.wait(1),
        events.no_block(
            events.move_cam_to_tile("handin", 43, 15, 3)
        ),
        events.move_npc("guard1", "handin", [
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "up",
        ]),
        events.wait(1),
        events.play("unlock"),
        events.no_block(
            events.write_to_tile(
                "handin",
                x=44,
                y=18,
                layer=0,
                tile=134,
                detail=120
            )
        ),
        events.write_to_tile(
            "handin",
            x=44,
            y=17,
            layer=0,
            tile=134,
            detail=104
        ),
        events.no_block(
            events.move_npc("guard1", "handin", [
                "up",
                "up",
                "up",
                "up",
                "up",
                "up",
            ]),
        ),
        events.wait(2),
        events.say("handin", "guard1", "Has the dayman gone?", 3),
        events.wait(1),
        events.say("handin", "gregor", "Yah.", 1),
        events.wait(1),
        events.say("handin", "guard1", "Good.", 1),
        events.wait(0.25),
        events.say("handin", "guard1",
                   "Marmil will want to see you in the tower.", 3.5),
        events.wait(1),
        events.say("handin", "gregor", "Let's go.", 2.5),
        events.wait(1),
        events.no_block(
            events.move_npc("gregor", "handin", [
                "down",
                "down",
                "down",
                "down",
                "down",
                "down",
                "down",
                "down",
            ]),
        ),
        events.no_block(
            events.move_npc("guard1", "handin", [
                "down",
                "down",
                "down",
                "down",
                "down",
                "down",
                "left",
                "left",
            ]),
        ),
        events.fade_in_screen(),
        events.replace_scene(
            "handin",
            {
                "map": "sewer",
                "seed": "sewer",
                "focus_x": 35,
                "focus_y": 15,
                "hide_hero": False,
            }
        ),
        events.hand_off("sewer")
    ]
    storboard = Storyboard(stack, cutscene, True)
    stack.push(storboard)
