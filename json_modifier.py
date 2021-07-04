from collections import abc


class ModifierRegistry:
    registry = {}

    def __init__(self, label):
        self.label = label

    def __call__(self, citizen):
        type(self).registry[self.label] = citizen
        return citizen

    @classmethod
    def is_modifier(cls, data):
        for modifier in cls.registry.values():
            if modifier.is_modifier(data):
                return True
        return False

    @classmethod
    def get_modifier(cls, store, data):
        for modifier in cls.registry.values():
            if modifier.is_modifier(data):
                return modifier(store, data)
        assert(False)


def process_json(data, store):
    for key, parent in find_modifiers(data):
        modifier = ModifierRegistry.get_modifier(store, parent[key])
        parent[key] = modifier.run()


def find_modifiers(data):
    modifiers = []
    find_modifiers_recursive(data, None, None, modifiers)
    return modifiers


def find_modifiers_recursive(data, parent, key, result):
    pointer = data
    if isinstance(pointer, abc.Mapping):
        if ModifierRegistry.is_modifier(pointer):
            result.append((key, parent))
        for key, value in pointer.items():
            find_modifiers_recursive(value, pointer, key, result)
    elif isinstance(pointer, abc.MutableSequence):
        for item in pointer:
            find_modifiers_recursive(item, None, None, result)


@ModifierRegistry("ref")
class Ref:
    def __init__(self, store, data):
        self.store = store
        self.data = data

    def run(self):
        ref = self.data["ref"]
        if ModifierRegistry.is_modifier(ref):
            modifier = ModifierRegistry.get_modifier(self.store, ref)
            index = modifier.run()
        else:
            index = ref

        value = self.store
        for key in index.split("."):
            value = value[key]

        return value

    @staticmethod
    def is_modifier(data):
        return isinstance(data, dict) and len(data) == 1 and "ref" in data
