from core.system import SystemEventDispatcher


class Context:
    _instance = None

    def __init__(self):
        self.input_manager = None
        self.sound_manager = None
        self.renderer = None
        self.camera = None
        self.info = None
        self.data = {}
        self.delta_time = 0
        self.event_dispatcher = SystemEventDispatcher()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
