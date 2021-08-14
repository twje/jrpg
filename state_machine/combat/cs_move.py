import math
from animation import Animation
from core import tween
from . import register_state


@register_state('cs_move')
class CSMove:
    def __init__(self, character, context):
        self.character = character
        self.entity = character.entity
        self.move_time = 0.3
        self.move_distance = 32

        self.tween = None
        self.animation = None
        self.pixel_x = None
        self.pixel_y = None

    def enter(self, params):
        self.move_time = params.get("time", self.move_time)
        self.move_distance = params.get("distance", self.move_distance)
        backfourth = params["dir"]

        anims = self.character.anims
        if "advance" not in anims:
            anims["advance"] = [self.entity.start_frame]

        frames = anims["advance"]
        direction = -1
        if self.character.facing == "right":
            frames = anims["retreat"]
            direction = 1

        direction *= backfourth
        self.animation = Animation(frames)

        # store current position
        self.pixel_x, self.pixel_y = self.entity.sprite.get_position()
        self.tween = tween.Tween(0, direction, self.move_time)

    def exit(self):
        pass

    def update(self, dt):
        self.animation.update(dt)
        self.entity.set_frame(self.animation.frame())

        self.tween.update(dt)
        value = self.tween.value
        x = self.pixel_x + (value * self.move_distance)
        y = self.pixel_y
        self.entity.x = math.floor(x)
        self.entity.y = math.floor(y)
        self.entity.sprite.set_position(x, y)

    def render(self, renderer):
        pass

    def is_finished(self):
        return self.tween.is_finished
