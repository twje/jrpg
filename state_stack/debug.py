from combat import actor
from graphics.menu.layout import Layout, PanelLayout
from combat.actor_xp_summary import ActorXPSummary
import colors

class DebugState:
    def __init__(self, stack, world):
        self.layout = Layout()
        self.layout.panels['test'] = PanelLayout(0, 42, 422, 77)
        actor_hero = world.party.members["hero"]
        self.summary = ActorXPSummary(actor_hero, self.layout, "test")
        self.summary.add_pop_up("Level Up!", colors.RED)
        self.summary.add_pop_up("asda!", colors.WHITE)

    def on_select(self,  index, item):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        self.summary.update(dt)
        return False

    def render(self, renderer):
        renderer.begin()
        self.summary.render(renderer)
        renderer.end()
