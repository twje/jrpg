from core import Context
from core.graphics import TextureAtlas
from graphics.UI import Panel
import utils


class PanelLayout:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Layout:
    def __init__(self):
        info = Context.instance().info
        self.panels = {
            "screen": PanelLayout(
                0,
                0,
                info.screen_width,
                info.screen_height,
            )
        }
        self.tile_size = 3
        self.panel_def = TextureAtlas.load_from_filepath(
            utils.lookup_texture_filepath("gradient_panel.png"),
            self.tile_size,
            self.tile_size
        )

    def create_panel(self, name):
        layout = self.panels[name]
        panel = Panel(self.panel_def.copy(), self.tile_size)
        panel.relative_position(
            layout.x,
            layout.y,
            layout.width,
            layout.height
        )
        return panel

    def debug_render(self, renderer):
        for name in self.panels:
            panel = self.create_panel(name)
            panel.render(renderer)

    def contract(self, name, hort=0, vert=0):
        panel = self.panels[name]
        panel.x += hort/2
        panel.y += vert/2
        panel.width -= hort
        panel.height -= vert

    def split_hort(self, name, tname, bname, y, split_size):
        parent = self.panels[name]
        del self.panels[name]

        half_split_size = split_size/2
        p1_height = parent.height * y
        p2_height = parent.height * (1 - y)

        # top panel
        self.panels[tname] = PanelLayout(
            x=parent.x,
            y=parent.y,
            width=parent.width,
            height=p1_height - half_split_size
        )

        # bottom panel
        self.panels[bname] = PanelLayout(
            x=parent.x,
            y=parent.y + p1_height + half_split_size,
            width=parent.width,
            height=p2_height - half_split_size
        )

    def split_vert(self, name, lname, rname, x, split_size):
        parent = self.panels[name]
        del self.panels[name]

        half_split_size = split_size/2
        p1_width = parent.width * x
        p2_width = parent.width * (1 - x)

        # top panel
        self.panels[lname] = PanelLayout(
            x=parent.x,
            y=parent.y,
            width=p1_width - half_split_size,
            height=parent.height
        )

        # bottom panel
        self.panels[rname] = PanelLayout(
            x=parent.x + p1_width + half_split_size,
            y=parent.y,
            width=p2_width - half_split_size,
            height=parent.height
        )

    def top(self, name):
        panel = self.panels[name]
        return panel.y

    def bottom(self, name):
        panel = self.panels[name]
        return panel.y + panel.height

    def left(self, name):
        panel = self.panels[name]
        return panel.x

    def right(self, name):
        panel = self.panels[name]
        return panel.x + panel.width

    def mid_x(self, name):
        panel = self.panels[name]
        return panel.x + panel.width/2

    def mid_y(self, name):
        panel = self.panels[name]
        return panel.y + panel.height/2

    def layout(self, name):
        return self.panels[name]