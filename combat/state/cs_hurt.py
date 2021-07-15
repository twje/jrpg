from . import register_state


@register_state('cs_hurt')
class CSHurt:
    def __init__(self, character, context):
        self.character = character
        self.combat_scene = context

    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass
