from entity import Entity
from animation import Animation


class AnimEntityFX:
    def __init__(self, x, y, entity_def, frames, spf=0.030):
        self.entity = Entity(entity_def)
        self.anim = Animation(frames, False, spf)
        self.priority = 2
        self.entity.x = x - self.entity.width/2
        self.entity.y = y - self.entity.height/2
        self.entity.sprite.set_position(self.entity.x, self.entity.y)

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        self.entity.render(renderer)

    def is_finished(self):
        return self.anim.is_finished()
