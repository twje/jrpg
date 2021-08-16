from core.graphics.sprite_font import Font, FontStyle
from graphics.UI import Selection
from graphics.UI import Panel
from core.graphics import TextureAtlas
from core.graphics import formatter
from core import Context
import utils
import pygame
import math

class BrowseListState:
    def __init__(self, stack, **kwargs):
        self.stack = stack
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.width = kwargs.get("width", 264)
        self.height = kwargs.get("height", 75)
        self.title = kwargs.get("title", "LIST")
        
        context = Context.instance()
        world = context.data["world"]        
        info = context.info        
        self.on_exit = kwargs.get("on_exit", lambda: None)
        self.on_focus = kwargs.get("on_focus", lambda item: None)
        self.up_arrow = world.icons.try_get("uparrow")
        self.down_arrow = world.icons.try_get("downarrow")
        self._hide = False

        data = kwargs.get("data", {})
        columns = kwargs.get("columns", 2)
        display_rows = kwargs.get("rows", 3)
        item_count = max(columns, len(data))
        max_rows = max(display_rows, math.ceil(item_count/columns))
        sellect_callback = kwargs.get("on_selection", lambda index, item: None)
        self.selection = Selection({
            "font": Font(style=FontStyle.small()),
            "data": data,
            "columns": columns,
            "display_rows": display_rows,
            "rows": max_rows,
            "spacing_x": 150,
            "spacing_y": 19,
            "on_selection": sellect_callback,
            "render_item": kwargs["on_render_item"]
        })
        
        self.selection.set_position(
            (info.screen_width - self.selection.width)/2,
            info.screen_height/3
        )

        pad = 10
        self.box = self.create_panel(
            self.selection.x - pad,
            self.selection.y - pad,
            self.selection.width + pad,
            self.selection.height + pad
        )
        self.set_arrow_position()
        

    def create_panel(self, x, y, width, height):
        tile_size = 3
        panel = Panel(
            TextureAtlas.load_from_filepath(
                utils.lookup_texture_filepath("gradient_panel.png"),
                tile_size,
                tile_size
            ),
            tile_size
        )
        panel.position(x, y, x + width, y + height)

        return panel

    def set_arrow_position(self):
        arrow_pad = 9
        arrow_x = self.x + self.width - arrow_pad
        self.up_arrow.set_position(arrow_x, self.y - arrow_pad)
        self.down_arrow.set_position(arrow_x, self.y - self.height + arrow_pad)

    def enter(self):
        self.on_focus(self.selection.selected_item())

    def exit(self):
        self.on_exit()

    def update(self, dt):
        pass

    def hide(self):
        self._hide = True

    def show(self):
        self._hide = False
        self.on_focus(self.selection.selected_item())

    def render(self, renderer):
        if self._hide:
            return

        self.box.render(renderer)
        self.render_arrows(renderer)
        self.selection.render(renderer)           

    def render_arrows(self, renderer):
        if self.selection.can_scroll_up():
            renderer.draw(self.up_arrow)
        if self.selection.can_scroll_down():
            renderer.draw(self.down_arrow)            

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.stack.pop()
            prev_index = self.selection.get_index()

            self.selection.handle_input(event)

            if prev_index != self.selection.get_index():
                self.on_focus(self.selection.selected_item())
