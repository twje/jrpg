from core.graphics import Sprite
from core import Context


class ScreenState:
    def __init__(self, color=(0, 0, 0)):
        self.square = type(self).new_surface(color)

    def set_alpha(self, alpha):
        self.square.set_alpha(alpha)

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        return True

    def render(self, renderer):
        renderer.begin()
        renderer.draw(self.square)
        renderer.end()

    @staticmethod
    def new_surface(color):
        context = Context.instance()
        return Sprite.create_rectangle(
            0,
            0,
            context.info.screen_width,
            context.info.screen_height,
            color
        )
