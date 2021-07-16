from collections.abc import MutableSequence
from weakref import ref


class WeakList(MutableSequence):
    def __init__(self):
        super().__init__()                
        self.items = []

    def __getitem__(self, key):
        return self.items[key]()

    def __setitem__(self, key, value):
        self.items[key] = self._get_weakref(value)

    def __delitem__(self, key):
        del self.items[key]

    def __len__(self):
        return len(self.items)

    def insert(self, index, value):
        self.items.insert(index, self._get_weakref(value))

    def _get_weakref(self, value):
        return ref(value, lambda item: self.items.remove(item))
