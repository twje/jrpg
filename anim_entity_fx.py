from entity import Entity
from animation import Animation


class AnimEntityFx:
    def __init__(self, x, y, entity_def, frames, spf=0.015):
        self.entity = Entity(entity_def)
        self.anim = Animation(frames, False, spf)
        self.priority = 2
        self.entity.x = x
        self.entity.y = y
        self.entity.sprite.set_position(x, y)

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        self.entity.render(renderer)

    def is_finished(self):
        return self.anim.is_finished()
