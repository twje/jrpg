from . import register_state
from core import Context
from graphics.menu import Layout
from graphics.UI import Selection
from core.graphics import SpriteFont
from core.graphics import formatter
import pygame


@register_state("frontmenu")
class FrontMenuState:
    def __init__(self, parent):
        self.parent = parent
        self.stack = parent.stack
        self.state_machine = parent.state_machine
        self.world = Context.instance().data["world"]

        self.layout = Layout()
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "top", "bottom", 0.12, 2)
        self.layout.split_vert("bottom", "left", "party", 0.3, 2)
        self.layout.split_hort("left", "menu", "gold", 0.7, 2)

        self.selection = Selection({
            "spacing_y": 32,
            "data": [
                "Items",
                "Magic",
                "Equipment",
                "Status",
                "Save"
            ],
            "on_selection": self.on_menu_click,
        })

        self.panels = [
            self.layout.create_panel("gold"),
            self.layout.create_panel("top"),
            self.layout.create_panel("party"),
            self.layout.create_panel("menu"),
        ]
        self.top_bar_text = "Current Map Name"

    def on_menu_click(self, index, item):
        if item == "Items":
            self.state_machine.change("items")

    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_input(self, event):
        self.selection.handle_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.stack.pop()

    def render(self, renderer):
        self.render_panals(renderer)
        self.render_menu(renderer)
        self.render_top(renderer)
        self.render_gold(renderer)

    def render_panals(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_menu(self, renderer):
        menu_layout = self.layout.layout("menu")
        self.selection.set_position(
            formatter.left_justify(0, menu_layout, self.selection),
            formatter.center_y(menu_layout, self.selection)
        )
        self.selection.render(renderer)

    def render_top(self, renderer):
        top_layout = self.layout.layout("top")
        text = SpriteFont(self.top_bar_text)
        text.set_position(
            formatter.center_x(top_layout, text),
            formatter.center_y(top_layout, text)
        )
        renderer.draw(text)

    def render_gold(self, renderer):
        gold_layout = self.layout.layout("gold")
        for index, (key, value) in enumerate({
            "Gold": self.world.gold,
            "Time": "{}".format(int(self.world.time)),
        }.items()):
            text = SpriteFont(self.stage_label(key, value))
            text.set_position(
                formatter.left_justify(25, gold_layout, text),
                formatter.vert_stack(
                    index,
                    5,
                    10,
                    gold_layout,
                    text
                )
            )
            renderer.draw(text)

    def create_sprite_font(self, text, x, y):
        sprite_font = SpriteFont(text)
        sprite_font.set_position(x, y)
        return sprite_font

    def stage_label(self, label, value):
        return "{}:{:>3}".format(label, value)
