from . import register_state
from core import Context
from graphics.menu import Layout
from core.graphics import SpriteFont
from core.graphics import formatter
from combat import Actor
from combat import ActorSummary
from graphics.UI import Selection
from graphics.UI import EnvelopePanel
import utils
import pygame


@register_state("status")
class StatusMenuState:
    def __init__(self, parent):
        # state
        self.parent = parent
        self.stack = parent.stack
        self.state_machine = parent.state_machine
        self.world = Context.instance().data["world"]

        # layout
        self.layout = Layout()
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "title", "bottom", 0.12, 2)

        # UI components
        self.panels = [
            self.layout.create_panel("title"),
            self.layout.create_panel("bottom"),
        ]

        # set on enter
        self.actor = None
        self.actor_summary = None
        self.equip_menu = None
        self.actions = None

    def enter(self, data):
        self.actor = data["actor"]
        self.actor_summary = ActorSummary(self.actor, {"show_xp": True})
        self.equip_menu = Selection({
            "data": self.actor.active_equip_slots,
            "columns": 1,
            "rows": len(self.actor.active_equip_slots),
            "spacing_y": 26,
            "render_item": self.actor.render_equipment
        })
        self.equip_menu.hide_cursor()

        self.actions = Selection({
            "data": self.actor.actions,
            "columns": 1,
            "rows": len(self.actor.actions),
            "spacing_y": 18,
            "render_item": self.render_action_item
        })
        self.actions.hide_cursor()
        self.actions_panel = EnvelopePanel(
            self.actions,
            utils.lookup_texture_filepath("gradient_panel.png"),
            3,
            10
        )

    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_input(self, event):
        if self.is_user_input(event):
            self.state_machine.change("frontmenu")

    def is_user_input(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE)
        return False

    def render(self, renderer):
        self.render_panels(renderer)
        self.render_status_label(renderer)
        self.render_actor_summary(renderer)
        self.render_xp(renderer)
        self.render_eqipment_menu(renderer)
        self.render_actor_stats(renderer)
        self.render_item_stats(renderer)
        self.render_action(renderer)

    def render_panels(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_status_label(self, renderer):
        layout = self.layout.layout("title")
        label = SpriteFont("Status")
        label.set_position(
            formatter.center_x(layout, label),
            formatter.center_y(layout, label),
        )
        renderer.draw(label)

    def render_actor_summary(self, renderer):
        layout = self.layout.layout("bottom")
        self.actor_summary.set_position(
            formatter.left_justify(10, layout, self.actor.portrait),
            formatter.top_justify(10, layout, self.actor.portrait),
        )
        self.actor_summary.render(renderer)

    def render_xp(self, renderer):
        layout = self.layout.layout("bottom")
        xp_str = "XP: {}/{}".format(self.actor.xp, self.actor.next_level_xp)
        label = SpriteFont(xp_str)
        label.set_position(layout.x + 280, layout.y + 68)
        renderer.draw(label)

    def render_eqipment_menu(self, renderer):
        layout = self.layout.layout("bottom")
        self.equip_menu.set_position(layout.x + 350, layout.y + 180)
        self.equip_menu.render(renderer)

    def render_actor_stats(self, renderer):
        layout = self.layout.layout("bottom")
        stats = self.actor.stats
        for index, stat in enumerate(Actor.ACTOR_STATS):
            label = Actor.ACTOR_STAT_LABELS[index]
            value = stats.get(stat)

            text = SpriteFont(f"{label}: {value}")
            text.set_position(
                80,
                formatter.vert_stack(
                    index,
                    100,
                    5,
                    layout,
                    text
                )
            )
            renderer.draw(text)

    def render_item_stats(self, renderer):
        layout = self.layout.layout("bottom")
        stats = self.actor.stats
        for index, stat in enumerate(Actor.ITEM_STATS):
            label = Actor.ITEM_STAT_LABELS[index]
            value = stats.get(stat)

            text = SpriteFont(f"{label}: {value}")
            text.set_position(
                80,
                formatter.vert_stack(
                    index,
                    190,
                    5,
                    layout,
                    text
                )
            )
            renderer.draw(text)

    def render_action(self, renderer):
        self.actions.set_position(450, 180)
        self.actions_panel.render(renderer)
        self.actions.render(renderer)

    def render_action_item(self, renderer, font, scale, x, y, item):
        label = Actor.ACTION_LABELS[item]
        sprite = SpriteFont(label)
        sprite.set_position(x, y)
        renderer.draw(sprite)
