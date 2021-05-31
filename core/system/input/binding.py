class Binding:
    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def update(self, event):
        for action in self.actions:
            action.update(event)

    def is_satisfied(self):
        return all(action.satisfied for action in self.actions)

    def clear(self):
        for action in self.actions:
            action.clear()
