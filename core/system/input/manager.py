class InputManager:
    def __init__(self):
        self.bindings = {}
        self.labels = set()

    def add_label(self, label):
        self.labels.add(label)

    def remove_label(self, label):
        try:
            self.labels.remove(label)
        except KeyError:
            pass

    def is_label_present(self, label):
        return label in self.labels

    def update(self, event):
        for binding in self.bindings.values():
            binding.update(event)

    def add_binding(self, name, binding):
        self.bindings[name] = binding

    def get_binding(self, name):
        return self.bindings[name]

    def clear(self):
        for binding in self.bindings.values():
            binding.clear()
