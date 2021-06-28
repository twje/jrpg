# """
# The InGameMenuState displays allows the player to navigate submenus
# """
from state_machine import StateMachine
from state_machine import NullState
from state_machine import state_registry


class InGameMenuState:
    def __init__(self, stack):
        self.stack = stack
        self.state_machine = StateMachine()
        self.state_machine.set_states({
            state: self.state_factory(state_registry.get(state))
            for state in [
                "frontmenu",
                "items",
                "magic",
                "equipment",
                "status"
            ]
        })
        self.state_machine.change("frontmenu")

    def state_factory(self, state):
        if state is None:
            return NullState()
        return lambda: state(self)

    def update(self, dt):
        if self.stack.is_on_top(self):
            self.state_machine.update(dt)
        return False

    def render(self, renderer):
        renderer.begin()
        self.state_machine.render(renderer)
        renderer.end()

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        self.state_machine.handle_input(event)
