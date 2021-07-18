from graphics.UI import create_fitted_textbox
from graphics.UI import create_fixed_textbox


class StateStack:
    def __init__(self):
        self.states = []

    def handle_input(self, event):
        top = self.top()
        if top is None:
            return

        top.handle_input(event)

    def update(self, dt):
        for state in reversed(self.states):
            update_prior_state = state.update(dt)
            if not update_prior_state:
                break

    def render(self, renderer):
        for state in self.states:
            state.render(renderer)

    def top(self):
        try:
            return self.states[-1]
        except IndexError:
            return

    def is_on_top(self, state):
        return self.top() == state

    def __len__(self):
        return len(self.states)

    def remove_top(self):
        self.states = self.states[:-1]

    def push(self, state):
        self.states.append(state)
        state.enter()

    def pop(self):
        top = self.top()
        self.remove_top()
        top.exit()
        return top

    def push_fitted(self, x, y, text_font, text, wrap=None,
                    title_font=None, title=None, avatar=None,
                    choices=None, on_finish=None):
        dialogue_box = create_fitted_textbox(
            self,
            x,
            y,
            text_font,
            text,
            wrap,
            title_font,
            title,
            avatar,
            choices,
            on_finish
        )
        self.states.append(dialogue_box)

    def push_fixed(self, x, y, width, height, text_font, text,
                   title_font=None, title=None, avatar=None,
                   choices=None, on_finish=None):
        dialogue_box = create_fixed_textbox(
            self,
            x,
            y,
            width,
            height,
            text_font,
            text,
            title_font,
            title,
            avatar,
            choices,
            on_finish
        )
        self.states.append(dialogue_box)
