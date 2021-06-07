# 460 - Displaying the Party in the In-Game Menu
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
from model import PartyModel
from combat import ActorSummary
from combat import Actor


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

        # TEST
        from state_stack.world import ExploreState
        from core import Camera
        from core import Context

        map_db = Context.instance().data["maps"]
        state = ExploreState(
            self.stack,
            Camera.create_camera_from_surface(
                Context.instance().info.surface
            ),
            map_db.new_map("arena"),
            30,
            18,
            0,
        )
        self.stack.push(state)

        # TEST
        model = PartyModel()
        self.world.party.add(Actor(model["hero"]))
        self.world.party.add(Actor(model["thief"]))
        self.world.party.add(Actor(model["mage"]))

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