from . import register_state


@register_state("npc_stand")
class NPCStand:
    def __init__(self, character, map):
        self.character = character
        self.map = map
        self.entity = character.entity
        self.controller = character.controller

    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self, renderer):
        pass
