from animation import Animation


class CSStandby:
    def __init__(self, character, context):
        self.character = character
        self.combat_scene = context
        self.entity = self.character.entity
        self.anim_id = None
        self.anim = None

    def enter(self, params):
        self.anim_id = params["anim"]
        frames = self.character.get_combat_anim(self.anim_id)
        self.anim = Animation(frames, params["loop"], params["spf"])

    def exit(self):
        pass

    def update(self, dt):
        self.anim.update(dt)
        self.entity.set_frame(self.anim.frame())

    def render(self, renderer):
        pass

    def is_finished(self):
        return self.anim.is_finished()