import random
from . import register_state


@register_state("plan_stroll")
class PlanStroll:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.entity = character.entity
        self.controller = character.controller

        self.frame_reset_speed = 0.05
        self.frame_count = 0

        self.count_down = random.randint(0, 3)

    def enter(self, data):
        self.frame_count = 0
        self.count_down = random.randint(0, 3)

    def exit(self):
        pass        

    def update(self, dt):
        self.count_down -= dt
        if self.count_down <= 0:
            choice = random.randint(0, 3)
            if choice == 0:
                self.controller.change("move", dict(x=-1, y=0))
            if choice == 1:
                self.controller.change("move", dict(x=0, y=-1))
            if choice == 2:
                self.controller.change("move", dict(x=1, y=0))
            if choice == 3:
                self.controller.change("move", dict(x=0, y=1))

        # reset frame to starting frame after a period of time
        if self.frame_count != -1:
            self.frame_count = self.frame_count + dt
            if self.frame_count >= self.frame_reset_speed:
                self.frame_count = -1
                self.entity.set_frame(self.entity.start_frame)
                self.character.facing = "down"

    def render(self, renderer):
        pass
