import math
from graphics.menu import Layout
from core.graphics import SpriteFont
from graphics.UI import Selection
from core.graphics import formatter
from item_db import items_db
from core.graphics.util import create_rect
from core import Context
import colors
import pygame


class LootSummaryState:
    def __init__(self, stack, world, combat_data):
        self.info = Context.instance().info
        self.stack = stack
        self.world = world
        self.loot = combat_data.get("loot", [])
        self.gold = combat_data.get("gold", 0)
        self.layout = Layout()
        self.panels = []
        self.gold_per_sec = 5
        self.gold_counter = 0
        self.is_counting_gold = True
        digit_number = math.log10(self.gold + 1)

        # init layout
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "top", "bottom", 0.25, 2)
        self.layout.split_hort("top", "title", "detail", 0.55, 2)
        self.layout.split_vert("detail", "left", "right", 0.5, 1)
        self.panels = [
            self.layout.create_panel("title"),
            self.layout.create_panel("left"),
            self.layout.create_panel("right"),
            self.layout.create_panel("bottom"),
        ]

        # init ui components
        self.background = create_rect(
            self.info.screen_width,
            self.info.screen_height, colors.BLACK
        )
        self.title = SpriteFont("Found Loot!")
        self.loot_view = Selection({
            "data": self.loot,
            "spacing_x": 175,
            "columns": 3,
            "rows": 9,
            "render_item": self.default_render_item,            
        })
        self.loot_view.set_position(
            self.layout.left("bottom"),
            self.layout.top("bottom") + 16
        )
        self.loot_view.hide_cursor()

        # style ui components
        title_panel = self.layout.layout("title")
        self.title.set_position(
            formatter.center_x(title_panel, self.title),
            formatter.center_y(title_panel, self.title)
        )

    def enter(self):
        self.is_counting_gold = True
        self.gold_counter = 0

        for item in self.loot:
            self.world.add_item(item["id"], item["count"])

    def exit(self):
        pass

    def skip_counting_gold(self):
        self.is_counting_gold = False
        self.gold_counter = 0
        gold_to_give = self.gold
        self.gold = 0
        self.world.gold += gold_to_give

    def handle_input(self, event):
        # hack - circular import
        from storyboard.storyboard import Storyboard
        from storyboard import events

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.gold > 0:
                    self.skip_counting_gold()
                    return

                self.stack.pop()
                self.storyboard = Storyboard(
                    self.stack,
                    [
                        events.black_screen("blackscreen", 1),
                        events.wait(0.1),
                        events.fade_out_screen("blackscreen", .2),
                    ]
                )
                self.storyboard.update(0)
                self.stack.push(self.storyboard)

    def update(self, dt):
        if self.is_counting_gold:
            self.gold_counter += self.gold_per_sec * dt
            gold_to_give = math.floor(self.gold_counter)
            self.gold_counter -= gold_to_give
            self.gold = max(0, self.gold - gold_to_give)

            self.world.gold += gold_to_give

            if self.gold == 0:
                self.is_counting_gold = False

        return False

    def render(self, renderer):
        renderer.begin()
        self.render_background(renderer)
        self.render_panels(renderer)
        self.render_title(renderer)
        self.render_found_gold(renderer)
        self.render_party_gold(renderer)
        self.render_loot_view(renderer)
        renderer.end()

    def render_background(self, renderer):
        renderer.draw(self.background)

    def render_panels(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_title(self, renderer):
        renderer.draw(self.title)

    def render_found_gold(self, renderer):
        panel = self.layout.layout("left")
        label = SpriteFont("Gold Found:")
        value = SpriteFont(f"{self.gold} gp")
        label.set_position(
            formatter.left_justify(12, panel, label),
            formatter.center_y(panel, label)
        )
        value.set_position(
            formatter.right_justify(0, panel, label),
            formatter.center_y(panel, value)
        )
        renderer.draw(label)
        renderer.draw(value)

    def render_party_gold(self, renderer):
        panel = self.layout.layout("right")
        label = SpriteFont("Party Gold:")
        value = SpriteFont(f"{self.world.gold} gp")
        label.set_position(
            formatter.left_justify(12, panel, label),
            formatter.center_y(panel, label)
        )
        value.set_position(
            formatter.right_justify(0, panel, label),
            formatter.center_y(panel, value)
        )
        renderer.draw(label)
        renderer.draw(value)

    def render_loot_view(self, renderer):
        self.loot_view.render(renderer)

    def default_render_item(self, renderer, font, scale, x, y, item):
        if item is None:
            return

        item_def = items_db[item["id"]]
        text = item_def["name"]

        if item["count"] > 1:
            text = f"{text} x{item['count']}"

        value = SpriteFont(text, font)
        value.set_position(x, y)

        renderer.draw(value)
