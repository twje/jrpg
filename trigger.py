def null_action(*args, **kwargs):
    pass


class Trigger:
    def __init__(self, trigger_def):
        self.on_enter = trigger_def.get("on_enter", null_action)
        self.on_exit = trigger_def.get("on_exit", null_action)
        self.on_use = trigger_def.get("on_use", null_action)
