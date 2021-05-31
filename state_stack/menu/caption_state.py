from core.graphics import SpriteFont
from core import Context


class LayoutAdapter:
    def __init__(self, x, y, surface):
        self.surface = surface
        self.x = x
        self.y = y

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()


class CaptionState:
    def __init__(self, text, font, layouter):
        self.sprite = SpriteFont(text, font)
        context = Context.instance()
        target = LayoutAdapter(0, 0, context.info.surface)
        layouter(target, self.sprite)

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
        renderer.draw(self.sprite)
        renderer.end()

    def set_alpha(self, alpha):
        self.sprite.set_alpha(alpha)
