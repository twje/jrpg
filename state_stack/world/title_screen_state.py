from core.graphics.sprite import Sprite
from core.graphics.sprite import Texture
from graphics.UI import Selection
from core.graphics import formatter
from core.graphics.sprite_font import Font, FontStyle
from core.graphics import SpriteFont
from core import Context
import utils


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


class TitleScreenState:
    def __init__(self, stack, storyboard):
        self.stack = stack
        self.storyboard = storyboard
        self.title_sprite = Sprite.load_from_filesystem(
            utils.lookup_texture_filepath("title_screen.png")
        )
        self.caption_sprite = SpriteFont("A min-rpg adventure")
        self.menu = Selection({
            "data": ["Play", "Exit"],
            "spacing_y": 32,
            "on_selection": self.on_selection
        })
        self.layout_ui()

    def layout_ui(self):
        context = Context.instance()
        target = LayoutAdapter(0, 0, context.info.surface)
        formatter.in_place_positon(0.5, 0.2, target, self.title_sprite)
        formatter.in_place_positon(0.5, 0.3, target, self.caption_sprite)
        formatter.in_place_positon(0.5, 0.6, target, self.menu)

    def on_selection(self, index, item):
        if index == 0:
            self.stack.pop()
            self.stack.push(self.storyboard)
        else:
            exit(0)        

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        self.menu.handle_input(event)

    def update(self, dt):
        return False

    def render(self, renderer):
        renderer.begin()
        renderer.draw(self.title_sprite)
        renderer.draw(self.caption_sprite)
        self.menu.render(renderer)
        renderer.end()
