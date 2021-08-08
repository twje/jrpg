from core.graphics.sprite_font import Font, FontStyle, SpriteFont
from graphics.UI import ProgressBar, progress_bar
from core.graphics import Sprite
from combat.xp_pop_up import XPPopUp
from core.graphics import formatter
import utils


class LayoutAdapter:
    def __init__(self, x, y, surface):
        self.surface = surface
        self.x = x
        self.y = y

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()


class ActorXPSummary:
    def __init__(self, actor, layout, layout_id):
        self.actor = actor
        self.layout = layout
        self.layout_id = layout_id
        self.pop_up_list = []
        self.pop_display_time = 1
        self.xp_bar = self.hp_bar = ProgressBar(
            {
                "value": actor.xp,
                "maximum": actor.next_level_xp,
                "background": Sprite.load_from_filesystem(
                    utils.lookup_texture_filepath("xpbackground.png")
                ),
                "foreground": Sprite.load_from_filesystem(
                    utils.lookup_texture_filepath("xpforeground.png")
                ),
            }
        )
        self.font = Font(FontStyle.small())
        self.avatar = actor.portrait
        self.avatar_name = SpriteFont(self.actor.name, self.font)

    def update(self, dt):
        popup = self.get_pop_up()
        if popup is None:
            return

        if popup.is_finished():
            self.pop_up_list.remove(popup)
            return

        popup.update(dt)
        if popup.display_time > self.pop_display_time and len(self.pop_up_list) > 1:
            popup.turn_off()

    def render(self, renderer):        
        self.render_avatar_portrait(renderer)
        self.render_avatar_name(renderer)
        self.render_level(renderer)
        self.render_xp(renderer)
        self.render_pop_up_box(renderer)

    def render_avatar_portrait(self, renderer):
        panel = self.layout.layout(self.layout_id)
        self.avatar.set_position(
            panel.x + 3,
            formatter.center_y(panel, self.avatar)
        )
        self.avatar_scale = 0.8
        self.avatar.scale_by_ratio(self.avatar_scale, self.avatar_scale)
        renderer.draw(self.avatar)

    def render_avatar_name(self, renderer):
        panel = self.layout.layout(self.layout_id)
        self.avatar_name.set_position(
            x=panel.x + self.avatar.width + 25,
            y=formatter.top_justify(3, panel, self.avatar_name) + 6
        )
        renderer.draw(self.avatar_name)

    def render_level(self, renderer):
        panel = self.layout.layout(self.layout_id)
        text = f"Level: {self.actor.level}"
        level_sprite = SpriteFont(text, self.font)
        level_sprite.set_position(
            x=panel.x + self.avatar.width + 25,
            y=formatter.bottom_justify(3, panel, self.avatar_name) - 6
        )
        renderer.draw(level_sprite)

    def render_xp(self, renderer):
        hort_pad = 9
        vert_pad = 3

        # EXP
        panel = self.layout.layout(self.layout_id)
        xp_label = SpriteFont("EXP:", self.font)
        xp_label.set_position(
            formatter.right_justify(vert_pad, panel, xp_label) - 100,
            formatter.top_justify(hort_pad, panel, xp_label)
        )
        xp_value = SpriteFont(str(self.actor.xp), self.font)
        xp_value.set_position(
            formatter.right_justify(vert_pad, panel, xp_label) - 18,
            formatter.top_justify(hort_pad, panel, xp_value)
        )
        renderer.draw(xp_label)
        renderer.draw(xp_value)

        # xp progress bar
        self.xp_bar.set_position(
            formatter.right_justify(vert_pad, panel, self.xp_bar) - 18,
            formatter.center_y(panel, self.xp_bar)
        )
        self.xp_bar.set_value(self.actor.xp, self.actor.next_level_xp)
        self.xp_bar.render(renderer)

        # Next Level
        next_level_label = SpriteFont("Next Level:", self.font)
        next_level_label.set_position(
            formatter.right_justify(vert_pad, panel, next_level_label) - 100,
            formatter.bottom_justify(hort_pad, panel, next_level_label)
        )
        next_level_value = SpriteFont(str(self.actor.next_level_xp), self.font)
        next_level_value.set_position(
            formatter.right_justify(vert_pad, panel, next_level_value) - 18,
            formatter.bottom_justify(hort_pad, panel, next_level_value)
        )
        renderer.draw(next_level_label)
        renderer.draw(next_level_value)

    def render_pop_up_box(self, renderer):
        popup = self.get_pop_up()
        if popup is not None:
            popup.render(renderer)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_pop_up(self, text, color):
        x = self.layout.mid_x(self.layout_id)
        y = self.layout.mid_y(self.layout_id)
        popup = XPPopUp(text, x, y, color)
        self.pop_up_list.append(popup)
        popup.turn_on()

    def pop_up_count(self):
        return len(self.pop_up_list)

    def cancel_pop_up(self):
        popup = self.get_pop_up()
        if popup is None:
            return

        if not popup.is_turning_off():
            popup.turn_off()

    def get_pop_up(self):
        if len(self.pop_up_list) > 0:
            return self.pop_up_list[0]
        return None
