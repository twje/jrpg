class DebuggerEvent:
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data


class Debugger:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def debug(self, kind, data):
        if kind == "storyboard":
            print(data)
