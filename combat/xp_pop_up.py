from core.graphics.sprite_font import Font, FontStyle
import utils
from core.tween import Tween
from core.graphics import TextureAtlas
from core.graphics import SpriteFont
from graphics.UI import Panel
import colors

class XPPopUp:
    def __init__(self, text, x, y, color=None):
        self.text = text
        self.x = x
        self.y = y
        self.color = colors.WHITE if color is None else color
        self.tween = None
        self.fade_time = 0.25
        self.display_time = 0
        self.tile_size = 3
        self.panel = Panel(
            TextureAtlas.load_from_filepath(
                utils.lookup_texture_filepath("gradient_panel.png"),
                self.tile_size,
                self.tile_size
            ),
            self.tile_size
        )        
        self.text_sprite = SpriteFont(text, Font(style=FontStyle.small()))
        self.text_sprite.set_color(self.color) 

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def turn_on(self):
        self.tween = Tween(0, 1, self.fade_time)

    def turn_off(self):
        current = self.tween.value
        self.tween = Tween(current, 0, current * self.fade_time)

    def is_turning_off(self):
        return self.tween.finished_value() == 0

    def update(self, dt):
        self.tween.update(dt)
        if self.tween.is_finished:
            self.display_time = min(5, self.display_time + dt)

    def is_finished(self):
        return self.tween.value == 0 and self.tween.finished_value() == 0

    def render(self, renderer):                
        # position
        padding = 10
        self.panel.center_position(
            self.x, 
            self.y, 
            self.text_sprite.width + padding, 
            self.text_sprite.height + padding
        )
        self.text_sprite.set_position(
            self.x - self.text_sprite.width/2, 
            self.y - self.text_sprite.height/2
        )
        
        # alpha
        alpha = self.tween.value         
        self.text_sprite.set_alpha(alpha)
        self.panel.set_alpha(alpha)

        # render
        self.panel.render(renderer)
        renderer.draw(self.text_sprite)