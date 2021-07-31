from . import register_state
from core.tween import Tween


@register_state('cs_die_enemy')
class CSEnemyDie:
    name = "cs_die"

    def __init__(self, character, context):
        self.character = character        
        self.sprite = character.entity.sprite        

        # on enter
        self.tween = None

    def enter(self, data):
        self.tween = Tween(1, 0, 1)

    def exit(self):
        pass

    def update(self, dt):
        self.tween.update(dt)
        alpha = self.tween.value
        self.sprite.set_alpha(alpha)

    def render(self, renderer):
        pass
        
    def is_finished(self):
        return self.tween.is_finished
