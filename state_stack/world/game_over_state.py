from core.graphics import formatter
from core.graphics.sprite_font import Font, FontStyle
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


class GameOverState:
    def __init__(self):
        self.game_over_sprite = SpriteFont(
            "Game Over", Font(FontStyle.storyboard_title())
        )
        self.continue_sprite = SpriteFont(
            "Want to find out what happens next? Write it!",
            Font(FontStyle.textbox_title())
        )

        # layout
        context = Context.instance()
        target = LayoutAdapter(0, 0, context.info.surface)

        formatter.in_place_positon(0.5, 0.3, target, self.game_over_sprite)
        formatter.in_place_positon(0.5, 0.5, target, self.continue_sprite)

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        return False

    def render(self, renderer):
        renderer.begin()
        renderer.draw(self.game_over_sprite)
        renderer.draw(self.continue_sprite)
        renderer.end()
