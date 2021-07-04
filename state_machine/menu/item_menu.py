from . import register_state
from item_db import items_db
from core import Context
from core.graphics import formatter
from core.graphics import FontStyle
from core.graphics import Font
from core.graphics import SpriteFont
from graphics.menu import Layout
from graphics.UI import ScrollBar
from graphics.UI import Selection
import utils
import pygame


@register_state("items")
class ItemMenuState:
    def __init__(self, parent):
        # state
        self.parent = parent
        self.stack = parent.stack
        self.state_machine = parent.state_machine
        self.world = Context.instance().data["world"]
        self.font = Font(style=FontStyle.default())
        self.in_category_menu = True

        # layout
        self.layout = Layout()
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "top", "bottom", 0.12, 2)
        self.layout.split_vert("top", "title", "category", 0.4, 2)
        self.layout.split_hort("bottom", "mid", "inv", 0.14, 2)

        # UI components
        self.panels = [
            self.layout.create_panel("title"),
            self.layout.create_panel("category"),
            self.layout.create_panel("mid"),
            self.layout.create_panel("inv"),
        ]
        self.scrollbar = ScrollBar(
            utils.lookup_texture_filepath("scrollbar.png"),
            18,
            self.layout.layout("inv").height
        )
        self.item_menus = [
            Selection({
                "data": self.world.items,
                "spacing_x": 256,
                "spacing_y": 28,
                "columns": 2,
                "display_rows": 8,
                "rows": 20,
                "render_item": self.world.render_item,
                "font": self.font,
            }),
            Selection({
                "data": self.world.key_items,
                "spacing_x": 256,
                "spacing_y": 28,
                "columns": 2,
                "display_rows": 8,
                "rows": 20,
                "render_item": self.world.render_key_item,
                "font": self.font,
            }),
        ]
        self.category_menu = Selection({
            "data": ["Use", "Key Items"],
            "spacing_x": 159,
            "columns": 2,
            "rows": 1,
            "on_selection": self.on_category_select,
            "font": self.font,
        })
        self.title_sprite = SpriteFont("Items", font=self.font)

        self.init_ui_components()

    def init_ui_components(self):
        # layouts
        inv_layout = self.layout.layout("inv")
        title_layout = self.layout.layout("title")
        category_layout = self.layout.layout("category")

        for menu in self.item_menus:
            menu.hide_cursor()
            menu.set_position(
                formatter.center_x(inv_layout, menu),
                formatter.center_y(inv_layout, menu),
            )
        self.category_menu.set_position(
            formatter.center_x(category_layout, self.category_menu),
            formatter.center_y(category_layout, self.category_menu),
        )
        self.title_sprite.set_position(
            formatter.center_x(title_layout, self.title_sprite),
            formatter.center_y(title_layout, self.title_sprite),
        )
        self.scrollbar.set_position(
            formatter.right_justify(0, inv_layout, self.scrollbar),
            formatter.top_justify(0, inv_layout, self.scrollbar),
        )

    def on_category_select(self, index, item):
        self.category_menu.hide_cursor()
        self.in_category_menu = False
        menu = self.item_menus[index]
        menu.show_cursor()

    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        self.update_scrollbar()  # needs a little love

    def update_scrollbar(self):
        scrolled = self.current_item_menu().percentage_scrolled()
        self.scrollbar.set_scroll_caret_scale(scrolled)
        self.scrollbar.set_normal(scrolled)

    def handle_input(self, event):
        if self.in_category_menu:
            self.handle_category_menu_input(event)
        else:
            self.handle_item_menu_input(event)

    def handle_category_menu_input(self, event):
        if self.is_exit_menu_event(event):
            self.state_machine.change("frontmenu")
        self.category_menu.handle_input(event)

    def handle_item_menu_input(self, event):
        if self.is_exit_menu_event(event):
            self.focus_on_category_menu()
        self.current_item_menu().handle_input(event)

    def focus_on_category_menu(self):
        self.in_category_menu = True
        self.current_item_menu().hide_cursor()
        self.category_menu.show_cursor()

    def is_exit_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key in (
                pygame.K_ESCAPE,
                pygame.K_BACKSPACE
            )
        return False

    def render(self, renderer):
        self.render_panels(renderer)
        self.render_title(renderer)
        self.render_description(renderer)
        self.render_inventory(renderer)
        self.render_scrollbar(renderer)

    def render_panels(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_inventory(self, renderer):
        menu = self.current_item_menu()
        menu.render(renderer)

    def render_title(self, renderer):
        self.category_menu.render(renderer)
        renderer.draw(self.title_sprite)

    def render_description(self, renderer):
        if self.in_category_menu:
            return

        item = self.selected_item()
        if item is not None:
            items_def = items_db[item.id]
            text = SpriteFont(items_def["description"], font=self.font)
            text.set_position(
                formatter.center_x(self.layout.layout("mid"), text),
                formatter.center_y(self.layout.layout("mid"), text),
            )
            renderer.draw(text)

    def render_scrollbar(self, renderer):
        self.scrollbar.render(renderer)

    def selected_item(self):
        return self.current_item_menu().selected_item()

    def current_item_menu(self):
        return self.item_menus[self.category_menu.get_index()]
