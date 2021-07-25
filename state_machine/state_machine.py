class NullState:
    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass

    def handle_input(self, event):
        pass


class StateMachine:
    def __init__(self):
        self.states = {}
        self.current = NullState()

    def set_state(self, state_id, state):
        self.states[state_id] = state

    def set_states(self, states):
        self.states = states

    def change(self, state_name, enter_params={}):
        if state_name not in self.states:
            raise Exception(f"state {state_name} must exist")
        self.current.exit()
        self.current = self.states[state_name]()
        self.current.enter(enter_params)

    def update(self, dt):
        self.current.update(dt)

    def render(self, renderer):
        self.current.render(renderer)

    def handle_input(self, event):
        self.current.handle_input(event)
