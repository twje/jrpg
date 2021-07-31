from . import register_state
from animation import Animation
from core.tween import Tween


@register_state('cs_hurt_enemy')
class CSEnemyHurt:
    # allows CSHurt and CSEnemyHurt to be used interchangeably
    name = "cs_hurt"

    def __init__(self, character, context):
        self.character = character
        self.entity = character.entity
        self.sprite = self.entity.sprite
        self.knock_back = 2              
        self.time = 2

        # on enter
        self.prev_state = None
        self.original_x = None
        self.original_y = None
        self.tween = None        

    def enter(self, data):
        self.prev_state = data["state"]

        pixel_pos = self.sprite.get_position()
        self.original_x = pixel_pos[0]
        self.original_y = pixel_pos[1]

        self.flash_color = None
        self.sprite.set_position(
            self.original_x - self.knock_back, 
            self.original_y
        )

        self.tween = Tween(0, 1, self.time)

    def exit(self):
        self.sprite.set_position(
            self.original_x,
            self.original_y
        )

    def update(self, dt):
        if self.tween.is_finished:
            self.character.controller.current = self.prev_state
            return

        self.tween.update(dt)
        self.value = self.tween.value

        self.sprite.set_position(
            self.original_x + self.knock_back * self.value,
            self.original_y
        )
        self.sprite.set_alpha(0.6 + self.value * 0.4)

    def render(self, renderer):
        pass
