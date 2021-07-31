from core.graphics import formatter
from core.graphics.sprite_font import Font, FontStyle
from core.graphics import SpriteFont
from core.graphics.util import create_rect
from graphics.UI import Selection
import colors
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
    def __init__(self, stack, world):
        self.context = Context.instance()
        self.stack = stack
        self.world = world
        self.menu = Selection({
            "data": ["New Game", "Continue"],
            "spacing_y": 36,
            "on_selection": self.on_select
        })
        self.background = create_rect(
            self.context.info.screen_width, 
            self.context.info.screen_height,
            colors.BLACK
        )
        self.title = SpriteFont(
            "Game Over", Font(FontStyle.title())
        )

        # layout
        self.context = Context.instance()
        self.context_layout = LayoutAdapter(0, 0, self.context.info.surface)
        formatter.in_place_positon(0.5, 0.25, self.context_layout, self.title)
        formatter.in_place_positon(0.5, 0.50, self.context_layout, self.menu)

    def on_select(self,  index, item):
        NEWGAME = 0
        CONTINUE = 1

        if index == NEWGAME:
            from world import World
            from state_stack.world import ExploreState
            from core import Camera

            # hack for now
            context = Context.instance()
            stack = context.data["stack"]            
            map_db = Context.instance().data["maps"]
            state = ExploreState(
                self.stack,
                Camera.create_camera_from_surface(
                    Context.instance().info.surface
                ),
                map_db.new_map("arena", "arena"),
                30,
                18,
                0,
            )
            stack.push(state)
        elif index == CONTINUE:
            print("No save system. No continue.")

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
        renderer.draw(self.background)
        renderer.draw(self.title)
        self.menu.render(renderer)
        renderer.end()
