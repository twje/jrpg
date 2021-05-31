from . import register_state
from animation import Animation
from entity import Entity


@register_state("sleep")
class SleepState:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.entity = character.entity
        self.controller = character.controller
        self.anim = Animation([0, 1, 2, 3], True, 0.6)
        self.sleep_entity = Entity.create_from_id("sleep")

        # set to default frame
        frames = getattr(self.character.anim, self.character.facing)
        self.entity.set_frame(frames[0])

    def enter(self, data):
        self.entity.add_child("snore", self.sleep_entity)

    def exit(self):
        self.entity.remove_child("snore")

    def update(self, dt):
        self.anim.update(dt)
        self.sleep_entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass
