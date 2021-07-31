from . import register_state
from animation import Animation


@register_state('cs_hurt_enemy')
class CSEnemyHurt:
    # allows CSHurt and CSEnemyHurt to be used interchangeably
    name = "cs_hurt"

    def __init__(self, character, context):
        self.character = character
        self.combat_scene = context
        self.entity = character.entity
        self.anim = None
        self.prev_state = None

    def enter(self, data):
        self.prev_state = data["state"]
        frames = self.character.get_combat_anim('hurt')
        self.anim = Animation(frames, False, 0.2)        
        self.entity.set_frame(self.anim.frame())

    def exit(self):
        pass

    def update(self, dt):
        if self.anim.is_finished():
            self.character.controller.current = self.prev_state
            return

        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass
