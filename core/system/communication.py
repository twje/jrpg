class SystemEvent:
    PLAY_SOUND = 0
    PLAY_MUSIC = 1
    

class SystemEventDispatcher:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, event, data={}):
        for observer in self.observers:
            observer.on_notify(event, data)
