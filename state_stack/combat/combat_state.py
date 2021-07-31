import copy
from collections import namedtuple
from utils import lookup_texture_filepath
from state_stack import StateStack
from core.graphics import Sprite
from core import Context
from character import Character
from graphics.UI import ProgressBar
from core.graphics import Font
from core.graphics import SpriteFont
from core.graphics import FontStyle
from core.graphics import formatter
from graphics.UI import Selection
from graphics.menu import Layout
from dependency import Injector
from dependency import Payload
from combat.event_queue import EventQueue
from combat.event import CETurn
from state_machine.combat import state_registry
import utils
import colors

ActorBar = namedtuple("ActorBar", "HP, MP")


class CombatStateUI:
    X_COL_SPAN = 200

    def __init__(self, state):
        self.state = state

        # font
        self.small_font = Font(FontStyle.small())

        # background
        self.background = Sprite.load_from_filesystem(
            lookup_texture_filepath(self.state.combat_def["background"])
        )

        # selection boxes
        self.party_list = Selection({
            "data": self.state.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.state.actors["party"]),
            "render_item": self.render_party_names,
            "on_selection": self.state.on_party_member_select,
            "font": self.small_font,
        })
        self.party_list.hide_cursor()

        self.stats_list = Selection({
            "data": self.state.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.state.actors["party"]),
            "render_item": self.render_party_stats,
            "on_selection": self.state.on_party_member_select,
            "font": self.small_font
        })
        self.stats_list.hide_cursor()

        # layout
        self.layout = Layout()
        self.layout.split_hort('screen', 'top', 'bottom', 0.72, 0)
        self.layout.split_hort('top', 'notice', 'top', 0.25, 0)
        self.layout.contract('notice', 75, 25)
        self.layout.split_hort('bottom', 'tip', 'bottom', 0.24, 0)
        self.layout.split_vert('bottom', 'left', 'right', 0.35, 0)

        # panels
        self.panels = [
            self.layout.create_panel("left"),
            self.layout.create_panel("right"),
        ]
        self.tip_panel = self.layout.create_panel('tip')
        self.notice_panel = self.layout.create_panel('notice')

        # panel titles
        self.panel_titles = [
            SpriteFont("NAME", font=self.small_font),
            SpriteFont("HP", font=self.small_font),
            SpriteFont("MP", font=self.small_font)
        ]

        # progress bars
        self.bars = {}
        for actor in self.state.actors["party"]:
            hp_bar = ProgressBar(
                {
                    "value": actor.stats.get("hp_now"),
                    "maximum": actor.stats.get("hp_max"),
                    "background": Sprite.load_from_filesystem(
                        utils.lookup_texture_filepath("hpbackground.png")
                    ),
                    "foreground": Sprite.load_from_filesystem(
                        utils.lookup_texture_filepath("hpforeground.png")
                    ),
                }
            )
            mp_bar = ProgressBar(
                {
                    "value": actor.stats.get("mp_now"),
                    "maximum": actor.stats.get("mp_max"),
                    "background": Sprite.load_from_filesystem(
                        utils.lookup_texture_filepath("mpbackground.png")
                    ),
                    "foreground": Sprite.load_from_filesystem(
                        utils.lookup_texture_filepath("mpforeground.png")
                    ),
                }
            )
            self.bars[actor] = ActorBar(hp_bar, mp_bar)

        self.init_ui()

    def init_ui(self):
        # layout variables
        left_layout = self.layout.layout('left')
        right_layout = self.layout.layout('right')
        y_margin = 4
        x_margin = 4
        content_top = left_layout.y + self.small_font.height() + y_margin

        # scale background
        self.background.scale_by_size(
            self.state.info.screen_width,
            self.state.info.screen_height
        )

        # position left panel title
        title_1 = self.panel_titles[0]
        title_1_x = formatter.center_x(left_layout, title_1)
        title_1.set_position(title_1_x, y_margin + left_layout.y)

        # position right panel titles
        right_margin = x_margin + self.party_list.cursor_width()
        right_titles = self.panel_titles[1:]
        for index, right_title in enumerate(right_titles):
            right_title.y = y_margin + right_layout.y
            right_title.x = right_margin + \
                right_layout.x + (index * self.X_COL_SPAN)

        # position party name selection box
        self.party_list.y = content_top
        self.party_list.align_hort(title_1_x)

        # position stat selection box
        self.stats_list.y = content_top
        self.stats_list.align_hort(right_titles[0].x)

    def render(self, renderer):
        self.render_background(renderer)
        self.render_party(renderer)
        self.render_enemy(renderer)
        self.render_effects(renderer)
        self.render_panels(renderer)
        self.render_panel_titles(renderer)
        self.render_selection_boxes(renderer)

    def render_background(self, renderer):
        renderer.draw(self.background)

    def render_party(self, renderer):
        for character in self.state.characters['party']:
            character.entity.render(renderer)

    def render_enemy(self, renderer):
        for character in self.state.characters['enemy']:
            character.entity.render(renderer)

        for character in self.state.death_list:
            character.entity.render(renderer)

    def render_effects(self, renderer):
        for effect in self.state.effects_list:
            effect.render(renderer)

    def render_panels(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_panel_titles(self, renderer):
        for panel_title in self.panel_titles:
            renderer.draw(panel_title)

    def render_selection_boxes(self, renderer):
        self.party_list.render(renderer)
        self.stats_list.render(renderer)

    def render_party_names(self, renderer, font, scale, x, y, item):
        sprite = SpriteFont(item.name, font=font)
        sprite.set_position(x, y)
        sprite.scale_by_ratio(scale, scale)

        if item == self.state.selected_actor:
            sprite.set_color((255, 255, 0))
        else:
            sprite.set_color((255, 255, 255))
        renderer.draw(sprite)

    def render_party_stats(self, renderer, font, scale, x, y, item):
        stats = item.stats
        bars = self.bars[item]
        bar_offset = 65

        self.render_hp(
            renderer,
            font,
            x,
            y,
            stats.get('hp_now'),
            stats.get('hp_max')
        )
        bars.HP.set_position(x + bar_offset, y)
        bars.HP.set_value(stats.get('hp_now'))
        bars.HP.render(renderer)

        x += self.X_COL_SPAN

        mp_sprite = SpriteFont(f"{stats.get('mp_now')}", font=font)
        mp_sprite.set_color(colors.WHITE)
        mp_sprite.set_position(x, y)
        renderer.draw(mp_sprite)
        bars.MP.set_position(x + bar_offset * .55, y)
        bars.MP.set_value(stats.get('mp_now'))
        bars.MP.render(renderer)

    def render_hp(self, renderer, font, x, y, hp_now, hp_max):
        percent = hp_now/hp_max

        hp_color = colors.WHITE
        if percent < 0.2:
            hp_color = (255, 0, 0)
        elif percent < 0.45:
            hp_color = (255, 255, 0)

        hp_now_sprite = SpriteFont(f"{hp_now}", font=font)
        hp_max_sprite = SpriteFont(f"/{hp_max}", font=font)

        hp_now_sprite.set_color(hp_color)
        hp_now_sprite.set_position(x, y)
        hp_max_sprite.set_position(x + hp_now_sprite.width, y)

        # hack
        hp_max_sprite.set_color(colors.WHITE)

        renderer.draw(hp_now_sprite)
        renderer.draw(hp_max_sprite)


class CombatState(Injector):
    # 0 - 1, each number is a percentage of with, hegiht offset from center of the screen
    LAYOUT = {
        "party": [
            [
                (0.25, -0.056, 0, 0)
            ],
            [
                (0.23, 0.024, 0, 0),
                (0.27, -0.136, 0, 0),
            ],
            [
                (0.73, 0.364, 0, 0),
                (0.75, 0.444, 0, 0),
                (0.77, 0.524, 0, 0),
            ]
        ],
        "enemy": [
            [
                (0.25, 0.56, 0, 0),
            ],
            [
                (0.25, 0.56, 0, 0),
                (0.25, 0.33, 0, 0),
            ],
            [
                (-0.21, -0.056, 0, 0),
                (-0.23, 0.024, 0, 0),
                (-0.27, -0.136, 0, 0),
            ],
            [
                (-0.18, -0.056, 0, 0),
                (-0.23, 0.056, 0, 0),
                (-0.25, -0.056, 0, 0),
                (-0.27, -0.168, 0, 0),
            ],
            [
                (-0.28, 0.032, 0, 0),
                (-0.3, -0.056, 0, 0),
                (-0.32, -0.144, 0, 0),
                (-0.2, 0.004, 0, 0),
                (-0.24, -0.116, 0, 0),
            ],
            [
                (-0.28, 0.032, 0, 0),
                (-0.3, -0.056, 0, 0),
                (-0.32, -0.144, 0, 0),
                (-0.16, 0.032, 0, 0),
                (-0.205, -0.056, 0, 0),
                (-0.225, -0.144, 0, 0),
            ]
        ]
    }

    def __init__(self, stack, combat_def):
        super().__init__()
        Character.register_as_dependency_injector(self)

        self.game_stack = stack
        self.combat_def = combat_def
        self.stack = StateStack()
        self.event_queue = EventQueue()
        self.context = Context.instance()
        self.entity_defs = self.context.data["entity_definitions"]
        self.info = self.context.info
        self.actors = {
            "party": self.combat_def["actors"]["party"],
            "enemy": self.combat_def["actors"]["enemy"],
        }
        self.characters = {
            "party": [],
            "enemy": []
        }
        self.selected_actor = None
        self.actor_char_map = {}
        self.death_list = []
        self.effects_list = []

        self.create_combat_characters("party")
        self.create_combat_characters("enemy")
        self.combat_ui = CombatStateUI(self)

    def get_dependency(self, identifier):
        if identifier == "combat_scene":
            return Payload(self)

    def add_effect(self, effect):
        for index, effect in enumerate(list(self.effects_list)):
            priority = effect.priority
            if effect.priority > priority:
                self.effects_list.insert(index + 1, effect)
                return
        self.effects_list.append(effect)

    def on_party_member_select(self, index, item):
        pass

    def create_combat_characters(self, side):
        actor_list = self.actors[side]
        character_list = self.characters[side]
        layout = self.LAYOUT[side][len(actor_list) - 1]

        for index, actor in enumerate(actor_list):
            character = self.actor_to_charcter(actor)

            self.actor_char_map[actor] = character
            position = layout[index]

            x = position[0] * self.info.screen_width
            y = position[1] * self.info.screen_height
            character.entity.sprite.set_position(x, y)

            # children position
            character.entity.x = x
            character.entity.y = y
            character.controller.change("cs_standby")

            character_list.append(character)

    def actor_to_charcter(self, actor):
        char_def = copy.copy(self.entity_defs.get_character_def(actor.id))
        char_def["entity"] = self.get_entity_combat_def(char_def)
        return Character(char_def, None)

    def get_entity_combat_def(self, char_def):
        if "combat_entity" in char_def:
            return char_def["combat_entity"]
        return char_def["entity"]

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        self.stack.handle_input(event)

    def update(self, dt):
        self.update_party(dt)
        self.update_enemy(dt)
        self.update_effects(dt)

        for character in list(self.death_list):
            character.controller.update(dt)
            state = character.controller.current

            if state.is_finished():
                self.death_list.remove(character)
        
        if len(self.stack) > 0:
            self.stack.update(dt)
        else:
            self.event_queue.update()

            self.add_turns(self.actors["party"])
            self.add_turns(self.actors["enemy"])

            if self.party_wins():
                self.event_queue.clear()
            elif self.enemy_wins():
                self.event_queue.clear()

        return False

    def update_party(self, dt):
         for character in self.characters["party"]:
            character.controller.update(dt)

    def update_enemy(self, dt):
        for character in self.characters["enemy"]:
            character.controller.update(dt)

    def update_effects(self, dt):
        for effect in list(self.effects_list):
            if effect.is_finished():
                self.effects_list.remove(effect)
            effect.update(dt)

    def add_turns(self, actor_list):
        for actor in actor_list:
            alive = actor.stats.get("hp_now") > 0

            if alive and not self.event_queue.actor_has_event(actor):
                event = CETurn(self, actor)
                tp = event.time_points(self.event_queue)
                self.event_queue.add(event, tp)

    def party_wins(self):
        return not self.has_live_actors(self.actors["enemy"])

    def enemy_wins(self):
        return not self.has_live_actors(self.actors["party"])

    def has_live_actors(self, actors):
        for actor in actors:
            if actor.stats.get("hp_now") > 0:
                return True
        return False

    def is_party_member(self, actor):
        return actor in self.actors["party"]

    def handle_death(self):
        self.handle_party_death()
        self.handle_enemy_death()

    def handle_party_death(self):
        actors = self.actors["party"]
        for actor in actors:
            character = self.actor_char_map[actor]
            controller = character.controller
            state = controller.current

            if isinstance(state, state_registry["cs_run_anim"]) and state.anim_id != "death":
                hp = actor.stats.get("hp_now")
                if hp <= 0:
                    controller.change("cs_run_anim", {"anim": "death"})
                    self.event_queue.removed_events_owned_by(actor)    

    def handle_enemy_death(self):
        actors = self.actors["enemy"]
        for actor in list(actors):
            hp = actor.stats.get("hp_now")
            if hp > 0:
                continue

            character = self.actor_char_map[actor]
            controller = character.controller

            # purge
            actors.remove(actor)
            self.characters["enemy"].remove(character)
            del self.actor_char_map[actor]

            controller.change("cs_die")
            self.event_queue.removed_events_owned_by(actor)

            # add to effects
            self.death_list.append(character)

    def render(self, renderer):
        renderer.begin()
        self.combat_ui.render(renderer)
        self.stack.render(renderer)
        self.event_queue.render(0, 0, renderer)
        renderer.end()
