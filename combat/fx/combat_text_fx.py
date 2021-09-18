from core.graphics import Font
from core.graphics import FontStyle
from core.graphics import SpriteFont
import colors


class CombatTextFX:
    def __init__(self, x, y, text, color=None):
        self.font = Font(FontStyle.small())
        self.x = x - self.font.width(text)/2
        self.y = y - self.font.height()/2
        self.color = colors.WHITE if color is None else color
        self.alpha = 1
        self.hold_time = 0.175
        self.hold_counter = 0
        self.fade_speed = 6
        self.priority = 0
        self.current_y = self.y
        self.velocity = 125
        self.gravity = 700
        self.font_sprite = SpriteFont(text, font=self.font)
        self.font_sprite.set_color(self.color)

    def is_finished(self):
        return self.alpha == 0

    def update(self, dt):
        self.current_y -= self.velocity * dt
        self.velocity -= self.gravity * dt
        self.font_sprite.set_position(self.x, self.current_y)

        if self.current_y >= self.y:
            self.current_y = self.y

            self.hold_counter += dt

            if self.hold_counter > self.hold_time:
                self.alpha = max(0, self.alpha - (dt * self.fade_speed))                
                self.font_sprite.set_alpha(self.alpha)  # check

    def render(self, renderer):
        renderer.draw(self.font_sprite)
