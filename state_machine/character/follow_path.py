from . import register_state


@register_state("follow_path")
class FollowPathState:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.tile_width = self.map.tile_width
        self.entity = character.entity
        self.controller = character.controller

    def enter(self, data):
        if self.character.is_path_complete():
            self.character.reset_default_state()
            return

        direction = self.character.path_direction()
        if direction == "left":
            return self.controller.change("move", dict(x=-1, y=0))
        if direction == "up":
            return self.controller.change("move", dict(x=0, y=-1))
        if direction == "right":
            return self.controller.change("move", dict(x=1, y=0))
        if direction == "down":
            return self.controller.change("move", dict(x=0, y=1))

        assert False

    def exit(self):
        self.character.increment_path()

    def update(self, dt):
        pass

    def render(self, renderer):
        pass
