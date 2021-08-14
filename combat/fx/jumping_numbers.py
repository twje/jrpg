from core.graphics import Font
from core.graphics import SpriteFont
from core.graphics import FontStyle
import colors


class JumpingNumbers:
    def __init__(self, x, y, number, color=None):
        self.font = Font(FontStyle.small())
        self.x = x - self.font.width(number)/2
        self.y = y - self.font.height()/2
        self.number = number
        self.color = colors.WHITE if color is None else color
        self.gravity = 700
        self.fade_distance = 33
        self.scale = 1
        self.priority = 0
        self.current_y = self.y
        self.velocity_y = 224
        self.font_sprite = SpriteFont(number, font=self.font)
        self.font_sprite.set_color(color)
        self.font_sprite.set_position(self.x, self.y)

    def update(self, dt):
        self.current_y = self.current_y - (self.velocity_y * dt)
        self.velocity_y = self.velocity_y - (self.gravity * dt)
        self.font_sprite.set_position(self.x, self.current_y)

        if self.current_y >= self.y:
            fade = min(1, (self.current_y - self.y)/self.fade_distance)
            self.font_sprite.set_alpha(1 - fade)

    def render(self, renderer):
        renderer.draw(self.font_sprite)

    def is_finished(self):
        return self.current_y >= (self.y + self.fade_distance)
