from state_stack import world
from core.graphics import util
from graphics.UI import Panel
from collections import namedtuple


class PanelLayout:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Layout:
    def __init__(self):
        self.panels = {
            "root": PanelLayout(
                0,
                0,
                10,
                10
            )
        }

    def vert_split_by_pad(self, name, lname, rname, widget, l_pad=None, t_pad=None, r_pad=None, b_pad=None):
        return 0, 0

    def vert_split_by_space(self, name, lname, rname, widget, x_space=None, y_space=None):
        return 0, 0


class Widget:
    def __init__(self):
        self.children = []
        self.x = 0
        self.y = 0

    def update(self, dt):
        self.update_hook(dt)
        for child in self.children:
            child.update(dt)

    def render(self, renderer):
        x = self.x
        y = self.y
        self.render_hook(renderer, x, y)
        for child in self.children:
            x += child.x
            y += child.y
            child.render_hook(renderer, x, y)

    def bounds(self):
        l = self.x
        t = self.y
        r = self.local_width
        b = self.local_height
        for child in self.children:
            l = min(l, child.x)
            t = min(t, child.y)
            r = max(r, child.x + child.local_width)
            b = max(b, child.y + child.local_height)

        return l, t, r, b

    @property
    def width(self):
        l, _, r, _ = self.bounds()
        return r - l

    @property
    def height(self):
        _, t, _, b = self.bounds()
        return b - t

    @property
    def local_width(self):
        return self.calc_width()

    @property
    def local_height(self):
        return self.calc_height()

    # -----
    # Hooks
    # -----
    def calc_width(self):
        pass

    def calc_height(self):
        pass

    def update_hook(self, dt):
        pass

    def render_hook(self, renderer, x_offset, y_offset):
        pass


class Textbox(Widget):
    def __init__(self):
        super().__init__()


class SpriteWidget(Widget):
    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite

    def calc_width(self):
        return self.sprite.width

    def calc_height(self):
        return self.sprite.height

    def render_hook(self, renderer, x_offset, y_offset):
        pass
        # self.sprite.x = x_offset
        # self.sprite.y = y_offset
        # renderer.draw(self.sprite)


Blueprint = namedtuple("Blueprint", "widget func data")


class TextboxBuilder:
    def __init__(self):
        self.product = Textbox()
        self.layout = Layout()
        

        # self.blueprints = {}
        # self.components = [
        #     "avatar",
        #     "title"
        # ]

    def add_avatar(self, avatar):
        widget = SpriteWidget(avatar)
        self.blueprints["avatar"] = Blueprint(
            widget,
            self.layout.vert_split_by_pad,
            [
                "root",
                "avatar",
                "root",
                widget
            ]
        )

    def debug_render(self, renderer):
        pass

    def build(self):
        for component in self.components:
            if component not in self.blueprints:
                continue

            blueprint = self.blueprints[component]
            x, y = blueprint.func(*blueprint.data)
            widget = blueprint.widget
            widget.x = x
            widget.y = y
            self.product.children.append(widget)
