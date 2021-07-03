class InputProcessor:
    def __init__(self, manager, label):
        self.manager = manager
        self.label = label
        self.manifest = []

    def bind_callback(self, name, callback):
        binding = self.manager.get_binding(name)
        self.manifest.append((binding, callback))

    def process(self):        
        for binding, callback in self.manifest:
            if binding.is_satisfied():
                callback()
                break

    def is_active(self):
        return self.manager.is_label_present(self.label)
