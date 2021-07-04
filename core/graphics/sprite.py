import pygame
from core.system.render import IRenderable
from core.graphics import Texture


# -------
# Sprites
# -------
class BaseSprite(IRenderable):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.angle = 0
        self.hotspot_x = 0
        self.hotspot_y = 0

    def set_color(self, color):
        self.texture.set_color(color)

    def set_alpha(self, alpha):
        self.texture.set_alpha(int(255 * alpha))

    def fill(self, color):
        self.texture.fill(color)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y    

    @property
    def width(self):
        self.validate()
        return self.texture.width

    @property
    def height(self):
        self.validate()
        return self.texture.height

    def scale_by_size(self, width, height):
        self.validate()
        self.texture.transform(
            self.hotspot_x,
            self.hotspot_y,
            self.angle,
            width,
            height
        )

    def scale_by_ratio(self, scale_width, scale_height):
        self.validate()
        self.texture.transform(
            self.hotspot_x,
            self.hotspot_y,
            self.angle,
            self.texture.original_width * scale_width,
            self.texture.original_height * scale_height,
        )

    # Renderable Interface
    def draw(self, surface, offset_x, offset_y):
        pos_x = self.x + offset_x
        pos_y = self.y + offset_y
        self.texture.draw(surface, pos_x, pos_y)


class Sprite(BaseSprite):
    def __init__(self, texture):
        super().__init__()
        self.texture = texture

    # Helper Methods
    def validate(self):
        if self.texture is None:
            raise Exception("Texture is not set")

    @classmethod
    def load_from_filesystem(cls, filepath):
        texture = Texture.load_from_filesystem(filepath)
        return cls(texture)

    @staticmethod
    def create_rectangle(x, y, width, height, color):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)
        sprite = Sprite(Texture(surface))
        sprite.set_position(x, y)
        return sprite


class SpriteAtlas(BaseSprite):
    def __init__(self, textureAtlas):
        super().__init__()
        self.textureAtlas = textureAtlas
        self.index = 0

    def update_texture(self, index):
        self.index = index

    def validate(self):
        if self.textureAtlas is None:
            raise Exception("TextureAtlas is not set")

    @property
    def texture(self):
        return self.textureAtlas[self.index]
