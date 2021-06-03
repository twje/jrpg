# 435 - Level-Up Test Program
from functools import partial
from core.graphics import formatter
from pipeline.util import convert_lua_to_json

from core import dirs
from core import Application

from core.system.input import InputProcessor
from state_stack import StateStack
from state_stack.world import TitleScreenState
import binding
import factory
from graphics.UI import Icons
from world import World
from map_db import MapDB
import utils

# TEST
from storyboard import Storyboard
from storyboard import events

# combat imports
from stats import Stat
from stats import StatID


class BlockState:
    def __init__(self, stack):
        self.stack = stack

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        if self.stack.is_on_top(self):
            self.stack.pop()

        return False

    def render(self, renderer):
        pass


class JRPG(Application):
    def load(self):
        binding.init(self.context.input_manager)
        self.input_processor = self.bind_input()
        self.init_managers()
        self.init_globals()

        self.scroll_speed = 10
        self.zoom_speed = 0.05
        self.stack = self.context.data["stack"]
        self.world = self.context.data["world"]

        # # combat ~ factor out too
        # self.stat = Stat({
        #     StatID.HP_NOW: 300,
        #     StatID.HP_MAX: 300,
        #     StatID.MP_NOW: 300,
        #     StatID.MP_MAX: 300,
        #     StatID.STRENGTH: 10,
        #     StatID.SPEED: 10,
        #     StatID.INTELLIGENCE: 10,
        # })

        # magic_hat = {
        #     "id": 1,
        #     "modifier": {
        #         "add": {
        #             StatID.STRENGTH: 5
        #         }
        #     }
        # }
        # magic_sword = {
        #     "id": 2,
        #     "modifier": {
        #         "add": {
        #             StatID.STRENGTH: 5
        #         }
        #     }
        # }
        # spell_bravery = {
        #     "id": "bravery",
        #     "modifier": {
        #         "mult": {
        #             StatID.STRENGTH: 0.1
        #         }
        #     }
        # }
        # spell_curse = {
        #     "id": "curse",
        #     "modifier": {
        #         "mult": {
        #             StatID.STRENGTH: -0.5
        #         }
        #     }
        # }

        # self.stat.add_modifier(magic_hat["id"], magic_hat["modifier"])
        # self.stat.add_modifier(magic_sword["id"], magic_sword["modifier"])
        # self.stat.add_modifier(spell_bravery["id"], spell_bravery["modifier"])
        # self.stat.add_modifier(spell_curse["id"], spell_curse["modifier"])

        # print(self.stat.get(StatID.STRENGTH))

        intro = [
            events.scene({
                "map": "sontos_house",
                "focus_x": 14,
                "focus_y": 19,
                "hide_hero": True
            }),
            events.black_screen(),
            events.wait(1),
            events.run_action(
                "AddNPC",
                {
                    "map": "sontos_house",
                    "definition": "sleeper",
                    "npc_id": "sleeper",
                    "tile_x": 14,
                    "tile_y": 19,
                },
                {
                    "map": events.get_map_ref
                }
            ),
            events.play("rain"),
            events.no_block(
                events.fade_sound("rain", 1, 0, 10)
            ),
            events.caption(
                "place",
                "title",
                "Village of Sontos",
                partial(formatter.in_place_positon, 0.5, 0.3)
            ),
            events.caption(
                "time",
                "subtitle",
                "MIDNIGHT",
                partial(formatter.in_place_positon, 0.5, 0.5)
            ),
            events.wait(2),
            events.no_block(
                events.fade_out_caption("place", 3)
            ),
            events.fade_out_caption("time", 3),
            events.kill_state("place"),
            events.kill_state("time"),
            events.fade_out_screen(),
            events.wait(2),
            events.fade_in_screen(),
            events.run_action(
                "AddNPC",
                {
                    "map": "sontos_house",
                    "definition": "guard",
                    "npc_id": "guard1",
                    "tile_x": 19,
                    "tile_y": 22,
                },
                {
                    "map": events.get_map_ref
                }
            ),
            events.wait(1),
            events.play("door_break"),
            events.no_block(events.fade_out_screen()),
            events.move_npc("guard1", "sontos_house", [
                "up", "up", "up",
                "left", "left", "left"
            ]),
            events.wait(1),
            events.say("sontos_house", "guard1", "Found you!", 2),
            events.wait(1),
            events.say("sontos_house", "guard1", "You're coming with me.", 2),
            events.fade_in_screen(),

            # kidnap
            events.no_block(events.play("bell")),
            events.wait(2.5),
            events.no_block(events.play("bell")),
            events.fade_sound("bell", 1, 0, 0.2),
            events.play('wagon'),
            events.no_block(events.fade_sound("wagon", 0, 1, 2)),
            events.play("wind"),
            events.no_block(events.fade_sound("wind", 0, 1, 2)),
            events.wait(3),
            events.caption(
                "time_passes",
                "title",
                "Two days later...",
                partial(formatter.in_place_positon, 0.5, 0.3)
            ),
            events.wait(1),
            events.fade_out_caption("time_passes", 3),
            events.kill_state("time_passes"),
            events.no_block(events.fade_sound("wind", 1, 0, 1)),
            events.no_block(events.fade_sound("wagon", 1, 0, 1)),
            events.wait(2),
            events.caption(
                "place",
                "title",
                "Unknown Dungeon",
                partial(formatter.in_place_positon, 0.5, 0.3)
            ),
            events.wait(2),
            events.fade_out_caption("place", 3),
            events.kill_state("place"),
            events.replace_scene(
                "sontos_house",
                {
                    "map": "jail",
                    "seed": "jail",
                    "focus_x": 56,
                    "focus_y": 11,
                    "hide_hero": False,
                }
            ),
            events.fade_out_screen(),
            events.wait(0.5),
            events.say("jail", "hero", "Where am I?", 3),
            events.wait(3),
            events.hand_off("jail")
        ]
        self.storyboard = Storyboard(self.stack, intro)
        titleState = TitleScreenState(self.stack, self.storyboard)
        self.stack.push(titleState)

    def init_managers(self):
        self.context.sound_manager.resolver = utils.lookup_sound_filepath

    def init_globals(self):
        self.store_in_context(
            "entity_definitions",
            factory.load_entity_definition()
        )

        self.manifest = self.store_in_context(
            "manifest",
            factory.load_manifest()
        )

        self.store_in_context(
            "icons",
            Icons()
        )

        self.store_in_context(
            "world",
            World()
        )

        self.store_in_context(
            "maps",
            MapDB("art/maps/database.json")
        )

        self.store_in_context(
            "stack",
            StateStack()
        )

    def bind_input(self):
        input_processor = InputProcessor(self.context.input_manager, "camera")

        # zoom world_camera
        input_processor.bind_callback("zoom_in", self.zoom_in)
        input_processor.bind_callback("zoom_out", self.zoom_out)

        return input_processor

    def handle_event(self, event):
        self.stack.handle_input(event)

    def update_hook(self, dt):
        self.input_processor.process()
        self.stack.update(dt)
        self.world.update(dt)

    def draw_hook(self, renderer):
        self.stack.render(renderer)

    def zoom_in(self):
        self.world_camera.increment_zoom(-self.zoom_speed)

    def zoom_out(self):
        self.world_camera.increment_zoom(self.zoom_speed)


if __name__ == "__main__":
    # content pipeline
    convert_lua_to_json(dirs)
    settings = factory.load_application_settings()

    # application logic
    game = JRPG(
        settings["name"],
        settings["width"],
        settings["height"]
    )
    game.run()
