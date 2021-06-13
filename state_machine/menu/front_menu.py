from . import register_state
from core import Context
from graphics.menu import Layout
from graphics.UI import Selection
from core.graphics import SpriteFont
from core.graphics import formatter
from combat import ActorSummary
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
        self.prev_top_bar_text = self.top_bar_text
        self.in_party_menu = False

        self.party_menu = Selection({
            "spacing_y": 90,
            "data": self.create_party_summaries(),
            "columns": 1,
            "rows": 3,
            "on_selection": self.on_party_member_chosen,
            "render_item": self.render_party_summary
        })
        self.party_menu.hide_cursor()

    def on_menu_click(self, index, item):
        if item == "Items":
            self.state_machine.change("items")
            return
        elif item == "Status":
            self.focus_party_menu()

    def create_party_summaries(self):
        party_membership = self.world.party.members.values()
        return [ActorSummary(actor, {"show_xp": True})
                for actor in party_membership]

    def on_party_member_chosen(self, index, actor_summary):
        # stage mapping
        menu_option_to_state_id = {
            "Status": "status"
        }
        menu_option = self.selection.get_item()

        # switch state
        state_id = menu_option_to_state_id[menu_option]
        self.state_machine.change(state_id, {
            "actor": actor_summary.actor
        })

    def enter(self, data):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_input(self, event):
        if self.in_party_menu:
            self.party_menu.handle_input(event)
            if self.is_user_input(event):
                self.unfocus_party_menu()
        else:
            self.selection.handle_input(event)
            if self.is_user_input(event):
                self.stack.pop()

    def unfocus_party_menu(self):
        self.selection.show_cursor()
        self.party_menu.hide_cursor()
        self.top_bar_text = self.prev_top_bar_text
        self.in_party_menu = False

    def focus_party_menu(self):
        self.in_party_menu = True
        self.selection.hide_cursor()
        self.party_menu.show_cursor()
        self.prev_top_bar_text = self.top_bar_text
        self.top_bar_text = "Choose a party member"

    def is_user_input(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE)
        return False

    def render(self, renderer):
        self.render_panals(renderer)
        self.render_menu(renderer)
        self.render_top(renderer)
        self.render_gold(renderer)
        self.render_party_menu(renderer)

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

    def render_party_menu(self, renderer):
        party_layout = self.layout.layout("party")
        self.party_menu.set_position(
            party_layout.x,
            party_layout.y + 30
        )
        self.party_menu.render(renderer)

    def render_party_summary(self, renderer, font, scale, x, y, item):
        if item is None:
            return
        item.set_position(x, y)
        item.render(renderer)

    def create_sprite_font(self, text, x, y):
        sprite_font = SpriteFont(text)
        sprite_font.set_position(x, y)
        return sprite_font

    def stage_label(self, label, value):
        return "{}:{:>3}".format(label, value)
