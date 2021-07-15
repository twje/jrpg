from animation import Animation


class CSStandby:
    def __init__(self, character, context):
        self.character = character
        self.combat_scene = context
        self.entity = self.character.entity
        self.anim = None

    def enter(self, params):
        frames = self.character.get_combat_anim("standby")
        self.anim = Animation(frames)

    def exit(self):
        pass

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass