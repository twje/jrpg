from state_stack import StateStack


class Storyboardevent:
    def __init__(self, operation):
        self.operation = operation
        self.event = None

    def update(self, storyboard, dt):
        if self.event is None:
            self.event = self.operation(storyboard)
        self.event.update(dt)

    def is_blocking(self):
        return self.event.is_blocking()

    def is_finished(self):
        return self.event.is_finished()


class Storyboard:
    def __init__(self, stack, events, hand_in=None):
        self.stack = stack
        self.events = [Storyboardevent(event) for event in events]
        self.states = {}
        self.sub_stack = StateStack()
        self.playing_sounds = {}

        if hand_in is not None:
            state = self.stack.pop()
            self.push_state("handin", state)

    def enter(self):
        pass

    def exit(self):
        for sound_id in self.playing_sounds.values():
            pass  # stop

    def handle_input(self, event):
        pass

    def update(self, dt):
        self.sub_stack.update(dt)

        if len(self.events) == 0:
            self.stack.pop()

        delete_index = None
        for index, event in enumerate(self.events):
            event.update(self, dt)
            if event.is_finished():
                delete_index = index
                break
            if event.is_blocking():
                break

        if delete_index is not None:
            del self.events[delete_index]

    def render(self, renderer):
        self.sub_stack.render(renderer)

    def add_sound(self, sound_id, sound):
        self.playing_sounds[sound_id] = sound

    def stop_sound(self, sound_id):
        sound = self.playing_sounds[sound_id]
        sound.stop()
        del self.playing_sounds[sound_id]

    def push_state(self, state_id, state):
        self.states[state_id] = state
        self.sub_stack.push(state)

    def remove_state(self, state_id):
        state = self.states[state_id]
        del self.states[state_id]
        self.sub_stack.states.remove(state)
