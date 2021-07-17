
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
import utils

ActorBar = namedtuple("ActorBar", "HP, MP")


class CombatStateUI:
    def __init__(self, state):
        self.state = state

        # selection boxes
        self.party_list = Selection({
            "data": self.state.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.actors["party"]),
            "render_item": self.render_party_names,
            "on_selection": self.on_party_member_select,
            "font": Font(FontStyle.small())
        })

        self.stats_list = Selection({
            "data": self.state.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.state.actors["party"]),
            "render_item": self.render_party_stats,
            "on_selection": self.on_party_member_select,
            "font": Font(FontStyle.small())
        })
        self.stats_list.hide_cursor()

        # layout
        layout = Layout()
        layout.split_hort('screen', 'top', 'bottom', 0.72, 0)
        layout.split_hort('top', 'notice', 'top', 0.25, 0)
        layout.contract('notice', 75, 25)
        layout.split_hort('bottom', 'tip', 'bottom', 0.24, 0)
        layout.split_vert('bottom', 'left', 'right', 0.33, 0)
        self.debug_layout = layout


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
                (-0.23, 0.024, 0, 0),
                (-0.27, -0.136, 0, 0),
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
        self.select_actor = None
        self.actor_char_map = {}

        # UI components
        self.stats_y_col = 208

        self.background = Sprite.load_from_filesystem(
            lookup_texture_filepath(self.combat_def["background"])
        )

        self.create_combat_characters("party")
        self.create_combat_characters("enemy")

        self.party_list = Selection({
            "data": self.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.actors["party"]),
            "render_item": self.render_party_names,
            "on_selection": self.on_party_member_select,
            "font": Font(FontStyle.small())
        })
        self.party_list.hide_cursor()

        self.stats_list = Selection({
            "data": self.actors["party"],
            "columns": 1,
            "spacing_x": 0,
            "spacing_y": 20,
            "rows": len(self.actors["party"]),
            "render_item": self.render_party_stats,
            "on_selection": self.on_party_member_select,
            "font": Font(FontStyle.small())
        })
        self.stats_list.hide_cursor()
        

        layout = Layout()
        layout.split_hort('screen', 'top', 'bottom', 0.72, 0)
        layout.split_hort('top', 'notice', 'top', 0.25, 0)
        layout.contract('notice', 75, 25)
        layout.split_hort('bottom', 'tip', 'bottom', 0.24, 0)
        layout.split_vert('bottom', 'left', 'right', 0.33, 0)
        self.layout = layout

        self.panels = [
            self.layout.create_panel("left"),
            self.layout.create_panel("right"),
        ]
        self.tip_panel = layout.create_panel('tip')
        self.notice_panel = layout.create_panel('notice')

        self.panel_title_font = Font(FontStyle.small())
        self.panel_titles = [
            SpriteFont("NAME", font=self.panel_title_font),
            SpriteFont("HP", font=self.panel_title_font),
            SpriteFont("MP", font=self.panel_title_font)
        ]
        # update panel title y position
        for panel_title in self.panel_titles:
            panel_title.y = layout.top('left') + 4

        # update panel title x position
        self.panel_titles[0].x = formatter.center_x(
            layout.layout('left'), self.panel_titles[0])
        formatter.in_place_multi_hort(
            layout.right('left'),
            30,
            [layout.layout('right').width/2, 0], self.panel_titles[1:]
        )

        self.party_list.set_position(
            layout.left('left') + 65,
            layout.top('left') + self.panel_title_font.height() + 5
        )

        # stat list position
        self.stats_list.set_position(
            layout.left('right'),
            layout.top('right') + 2 + self.panel_title_font.height() + 5
        )

        # progress bar
        self.bars = {}
        for actor in self.actors["party"]:
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

    def get_dependency(self, identifier):
        if identifier == "combat_scene":
            return Payload(self)

    def init_ui(self):
        self.background.scale_by_size(
            self.info.screen_width, self.info.screen_height)

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

        # override with combat entity
        if "combat_entity" in char_def:
            char_def["entity"] = char_def["combat_entity"]

        return Character(char_def, None)

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        for character in self.characters["party"]:
            character.controller.update(dt)

        for character in self.characters["enemy"]:
            character.controller.update(dt)

        return False

    def render(self, renderer):
        renderer.begin()
        self.render_background(renderer)
        self.layout.debug_render(renderer)
        self.render_party(renderer)
        self.render_enemy(renderer)
        self.render_panel_titles(renderer)
        self.render_party_name_selection(renderer)
        self.render_party_stats_selection(renderer)
        renderer.end()

    def render_background(self, renderer):
        renderer.draw(self.background)

    def render_party(self, renderer):
        for character in self.characters['party']:
            character.entity.render(renderer)

    def render_enemy(self, renderer):
        for character in self.characters['enemy']:
            character.entity.render(renderer)

    def render_panel_titles(self, renderer):
        for panel_title in self.panel_titles:
            sprite = SpriteFont(panel_title.text, font=self.panel_title_font)
            sprite.set_position(
                panel_title.x,
                panel_title.y
            )
            renderer.draw(sprite)

    def render_party_name_selection(self, renderer):
        self.party_list.render(renderer)

    def render_party_stats_selection(self, renderer):
        self.stats_list.render(renderer)

    def render_party_stats(self, renderer, font, scale, x, y, item):
        stats = item.stats
        bars = self.bars[item]
        bar_offset = 65

        self.render_hp(renderer, font, x, y, stats.get('hp_now'), stats.get('hp_max'))
        bars.HP.set_position(x + bar_offset, y)
        bars.HP.set_value(stats.get('hp_now'))
        bars.HP.render(renderer)

        x += 245

        mp_sprite = SpriteFont(f"{stats.get('mp_now')}", font=font)
        mp_sprite.set_position(x, y)
        renderer.draw(mp_sprite)
        bars.MP.set_position(x + bar_offset * .55, y)
        bars.MP.set_value(stats.get('mp_now'))
        bars.MP.render(renderer)

    def render_hp(self, renderer, font, x, y, hp_now, hp_max):
        percent = hp_now/hp_max

        # change color

        sprite = SpriteFont(f"{hp_now}/{hp_max}", font=font)
        sprite.set_position(x, y)
        renderer.draw(sprite)

    def render_party_names(self, renderer, font, scale, x, y, item):
        if item == self.select_actor:
            pass  # fix
        else:
            sprite = SpriteFont(item.name, font=font)
            sprite.set_position(x, y)
            sprite.scale_by_ratio(scale, scale)
            renderer.draw(sprite)
