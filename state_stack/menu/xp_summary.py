import math
from core.graphics import SpriteFont
from combat.actor_xp_summary import ActorXPSummary
from core.graphics import formatter
from graphics.menu import Layout
from core.graphics.util import create_rect
from core import Context
import colors
import pygame


class XPSummaryState:
    def __init__(self, stack, party, combat_data):
        self.stack = stack
        self.party = party
        self.combat_data = combat_data
        self.layout = Layout()
        self.xp = combat_data["xp"]
        self.xp_per_sec = 5
        self.xp_counter = 0
        self.is_counting_xp = True
        self.party = party
        self.party_summary = []
        self.context = Context.instance()
        self.info = self.context.info
        self.world = self.context.data["world"]

        # init experience growth rate
        digit_number = math.log10(self.xp + 1)
        self.xp_per_sec *= (digit_number ** digit_number)

        # init layout
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "top", "bottom", 0.5, 2)
        self.layout.split_hort("top", "top", "one", 0.5, 2)
        self.layout.split_hort("bottom", "two", "three", 0.5, 2)
        self.layout.split_hort("top", "title", "detail", 0.5, 2)
        self.title_panels = [
            self.layout.create_panel("title"),
            self.layout.create_panel("detail")
        ]
        self.actor_panels = [
            self.layout.create_panel("one"),
            self.layout.create_panel("two"),
            self.layout.create_panel("three")
        ]

        # init party xp layout
        panel_ids = ["one", "two", "three"]
        for panel_id, actor in enumerate(self.party):
            summary = ActorXPSummary(actor, self.layout, panel_ids[panel_id])
            self.party_summary.append(summary)

        # init ui components
        self.background = create_rect(
            self.info.screen_width,
            self.info.screen_height, colors.BLACK
        )
        self.title = SpriteFont("Experience Increased!")

        # style ui components
        title_panel = self.layout.layout("title")
        self.title.set_position(
            formatter.center_x(title_panel, self.title),
            formatter.center_y(title_panel, self.title)
        )

    def enter(self):
        pass

    def exit(self):
        pass

    def apply_xp_to_party(self, xp):
        for index, actor in enumerate(self.party):
            if actor.stats.get("hp_now") > 0:
                summary = self.party_summary[index]
                actor.add_xp(xp)
                while(actor.ready_to_level_up()):
                    level_up = actor.create_level_up()
                    level_number = actor.level + level_up["level"]
                    summary.add_pop_up(
                        f"Level Up {level_number}!", colors.YELLO)
                    actor.apply_level(level_up)

    def are_pop_ups_remianing(self):
        for summary in self.party_summary:
            if summary.pop_up_count() > 0:
                return True
        return False

    def close_next_pop_up(self):
        for summary in self.party_summary:
            if summary.pop_up_count() > 0:
                summary.cancel_pop_up()

    def skip_counting_xp(self):
        self.is_counting_xp = False
        self.xp_counter = 0
        xp_to_apply = self.xp
        self.xp = 0
        self.apply_xp_to_party(xp_to_apply)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.xp > 0:
                    self.skip_counting_xp()
                    return

                if self.are_pop_ups_remianing():
                    self.close_next_pop_up()
                    return

                self.goto_loot_summary()

    def goto_loot_summary(self):
        # hack - circular imports
        from state_stack.menu import LootSummaryState  
        from storyboard.storyboard import Storyboard
        from storyboard import events

        world = self.context.data["world"]
        loot_summary_state = LootSummaryState(
            self.stack, world, self.combat_data)

        self.storyboard = Storyboard(
            self.stack,
            [                
                events.black_screen("blackscreen"),
                events.fade_in_screen("blackscreen", 0.2),
                events.replace_state(self, loot_summary_state),
                events.wait(0.1),
                events.fade_out_screen("blackscreen", .2),
            ]
        )
        self.stack.push(self.storyboard)

    def update(self, dt):
        for summary in self.party_summary:
            summary.update(dt)

        if self.is_counting_xp:
            self.xp_counter += self.xp_per_sec * dt
            xp_to_apply = math.floor(self.xp_counter)
            self.xp_counter -= xp_to_apply
            self.xp = max(0, self.xp - xp_to_apply)
            self.apply_xp_to_party(xp_to_apply)

            if self.xp == 0:
                self.is_counting_xp = False

        return False

    def render(self, renderer):
        renderer.begin()
        self.render_background(renderer)
        self.render_title_panels(renderer)
        self.render_title(renderer)
        self.render_detail(renderer)
        self.render_party_summaries(renderer)
        renderer.end()

    def render_background(self, renderer):
        renderer.draw(self.background)

    def render_title_panels(self, renderer):
        for panel in self.title_panels:
            panel.render(renderer)

    def render_title(self, renderer):
        renderer.draw(self.title)

    def render_detail(self, renderer):
        panel = self.layout.layout("detail")
        text_sprite = SpriteFont(f"XP increased by {self.xp}")
        text_sprite.set_position(
            formatter.left_justify(15, panel, text_sprite),
            formatter.center_y(panel, text_sprite)
        )
        renderer.draw(text_sprite)

    def render_party_summaries(self, renderer):
        for panel_id, party_summary in enumerate(self.party_summary):
            panel = self.actor_panels[panel_id]
            panel.render(renderer)
            party_summary.render(renderer)
