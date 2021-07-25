from animation import Animation
from . import register_state


@register_state('cs_standby')
class CSStandby:
    def __init__(self, character, context):        
        self.character = character
        self.combat_scene = context
        self.entity = self.character.entity
        self.anim = None

    def enter(self, data):
        frames = self.character.get_combat_anim("standby")
        self.anim = Animation(frames)

    def exit(self):
        pass

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass
