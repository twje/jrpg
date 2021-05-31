from . import register_state
from core import Context
from core.system.input import InputProcessor


@register_state("wait")
class WaitState:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.entity = character.entity
        self.controller = character.controller
        self.input_processor = self.bind_input()
        self.frame_reset_speed = 0.05
        self.frame_count = 0

    def bind_input(self):
        input_processor = InputProcessor(
            Context.instance().input_manager,
            "move"
        )
        input_processor.bind_callback("move_left", self.move_left)
        input_processor.bind_callback("move_right", self.move_right)
        input_processor.bind_callback("move_up", self.move_up)
        input_processor.bind_callback("move_down", self.move_down)

        return input_processor

    def enter(self, data):
        self.frame_count = 0

    def exit(self):
        pass

    def update(self, dt):
        if not self.input_processor.is_active():
            return
        self.input_processor.process()

        # reset frame to starting frame after a period of time
        if self.frame_count != -1:
            self.frame_count = self.frame_count + dt
            if self.frame_count >= self.frame_reset_speed:
                self.frame_count = -1
                self.entity.set_frame(self.entity.start_frame)
                self.character.facing = "down"

    def render(self, renderer):
        pass

    # callbacks
    def move_left(self):
        self.controller.change("move", dict(x=-1, y=0))

    def move_up(self):
        self.controller.change("move", dict(x=0, y=-1))

    def move_right(self):
        self.controller.change("move", dict(x=1, y=0))

    def move_down(self):
        self.controller.change("move", dict(x=0, y=1))
