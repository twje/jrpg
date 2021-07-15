from . import register_state
from core.tween import Tween
from animation import Animation


@register_state("move")
class MoveState:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.tile_width = self.map.tile_width
        self.entity = character.entity
        self.controller = character.controller
        self.move_x = 0
        self.move_y = 0
        self.tween = Tween(0, 0, 1)
        self.move_speed = 0.3
        self.anim = Animation([self.entity.start_frame])

    def enter(self, data):
        x = data["x"]
        y = data["y"]

        # update animation
        if x == -1:
            frames = self.character.anims["left"]
            self.character.facing = "left"
        elif x == 1:
            frames = self.character.anims["right"]
            self.character.facing = "right"
        elif y == -1:
            frames = self.character.anims["up"]
            self.character.facing = "up"
        elif y == 1:
            frames = self.character.anims["down"]
            self.character.facing = "down"

        self.anim.set_frames(frames)

        # update movement
        self.move_x = x
        self.move_y = y
        self.pixel_x = self.entity.sprite.x
        self.pixel_y = self.entity.sprite.y
        self.tween = Tween(0, self.tile_width, self.move_speed)

        # collision detection
        target_x = self.entity.tile_x + x
        target_y = self.entity.tile_y + y

        if self.map.is_blocked(0, target_x, target_y):
            self.move_x = 0
            self.move_y = 0
            self.entity.set_frame(self.anim.frame())
            self.controller.change(self.character.default_state)
            return

        # exit trigger
        self.try_trigger_on_exit()

        # mark destination tile as occupied
        self.entity.set_tile_pos(
            self.entity.tile_x + self.move_x,
            self.entity.tile_y + self.move_y,
            self.entity.layer,
            self.map
        )
        self.entity.sprite.set_position(self.pixel_x, self.pixel_y)

    def exit(self):
        self.try_trigger_on_enter()

    def update(self, dt):
        # animation
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

        # movement
        self.tween.update(dt)

        value = self.tween.value
        x = self.pixel_x + (value * self.move_x)
        y = self.pixel_y + (value * self.move_y)
        self.entity.sprite.set_position(x, y)

        if self.tween.is_finished:
            self.controller.change(self.character.default_state)

    def render(self, renderer):
        pass

    # --------------
    # Helper Methods
    # --------------
    def try_trigger_on_exit(self):
        if self.move_x != 0 or self.move_y != 0:
            trigger = self.map.get_trigger(
                self.entity.layer,
                self.entity.tile_x,
                self.entity.tile_y,
            )
            if trigger is not None:
                trigger.on_exit(
                    trigger,
                    self.entity,
                    self.entity.layer,
                    self.entity.tile_x,
                    self.entity.tile_y
                )

    def try_trigger_on_enter(self):
        trigger = self.map.get_trigger(
            self.entity.layer,
            self.entity.tile_x,
            self.entity.tile_y,
        )
        if trigger is not None:
            trigger.on_enter(
                trigger,
                self.entity,
                self.entity.layer,
                self.entity.tile_x,
                self.entity.tile_y
            )
