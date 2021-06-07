from core.system.input import action
from graphics.UI import ProgressBar
from core.graphics import Sprite
from core.graphics import SpriteFont
import utils


class ActorSummary:
    def __init__(self, actor, params):
        self.x = 0
        self.y = 0
        self.width = 340
        self.actor = actor
        self.hp_bar = ProgressBar(
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
        self.mp_bar = ProgressBar(
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
        self.avatar_text_pad = 14
        self.label_right_pad = 15
        self.label_value_pad = 45
        self.vertical_pad = 18
        self.show_xp = params["show_xp"]

        if self.show_xp:
            self.xp_bar = ProgressBar({
                "value": actor.xp,
                "maximum": actor.next_level_xp,
                "background": Sprite.load_from_filesystem(
                    utils.lookup_texture_filepath("xpbackground.png")
                ),
                "foreground": Sprite.load_from_filesystem(
                    utils.lookup_texture_filepath("xpforeground.png")
                ),
            })

    @property
    def height(self):
        return self.po

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_cursor_position(self):
        raise Exception("not implemented")

    def render(self, renderer):
        # position avatar image top left
        avatar = self.actor.portrait
        avatar_width = self.actor.portrait.width
        avatar_x = self.x
        avatar_y = self.y
        avatar.set_position(avatar_x, avatar_y)
        renderer.draw(avatar)

        # name
        name_font_sprite = SpriteFont(self.actor.name)
        text_pad_y = 2
        text_x = avatar_x + avatar_width + self.avatar_text_pad
        text_y = self.y + text_pad_y
        name_font_sprite.set_position(text_x, text_y)
        renderer.draw(name_font_sprite)

        # LVL, HP and MP labels
        lvz_label = SpriteFont("LVZ")
        hp_label = SpriteFont("HP")
        mp_label = SpriteFont("MP")
        text_x = text_x + self.label_right_pad
        text_y = text_y + 20
        stats_start_y = text_y
        lvz_label.set_position(text_x, text_y)
        renderer.draw(lvz_label)
        text_y = text_y + self.vertical_pad
        hp_label.set_position(text_x, text_y)
        renderer.draw(hp_label)
        text_y = text_y + self.vertical_pad
        mp_label.set_position(text_x, text_y)
        renderer.draw(mp_label)

        # LVL, HP and MP values
        lvz_value = SpriteFont(str(self.actor.level))
        text_y = stats_start_y
        text_x = text_x + self.label_value_pad
        lvz_value.set_position(text_x, text_y)
        renderer.draw(lvz_value)

        hp = self.actor.stats.get("hp_now")
        max_hp = self.actor.stats.get("hp_max")
        hp_value = SpriteFont(f"{hp}/{max_hp}")
        text_y = text_y + self.vertical_pad
        hp_value.set_position(text_x, text_y)
        renderer.draw(hp_value)

        mp = self.actor.stats.get("mp_now")
        mp_now = self.actor.stats.get("mp_max")
        mp_value = SpriteFont(f"{mp}/{mp_now}")
        text_y = text_y + self.vertical_pad
        mp_value.set_position(text_x, text_y)
        renderer.draw(mp_value)

        # next level area
        if self.show_xp:
            next_level_label = SpriteFont("Next Level")
            bar_x = self.x + self.width * 0.8
            bar_y = self.y + 44
            self.xp_bar.set_position(bar_x, bar_y)
            self.xp_bar.render(renderer)
            next_level_label.set_position(bar_x, stats_start_y)
            renderer.draw(next_level_label)

        # MP & HP bars
        bar_x = self.x + avatar_width + self.avatar_text_pad
        bar_x = bar_x + self.label_right_pad + self.label_value_pad
        self.hp_bar.set_position(bar_x, self.y + 52)
        self.mp_bar.set_position(bar_x, self.y + 72)
        self.hp_bar.render(renderer)
        self.mp_bar.render(renderer)
