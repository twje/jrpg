"""
Textures are a base abstraction to be used by other higher level classes such as Sprite
"""
import pygame


class Texture:
    def __init__(self, surface):
        super().__init__()
        self.original_image = surface
        self.image = surface
        self._width = surface.get_size()[0]
        self._height = surface.get_size()[1]

    def fill(self, color):
        self.original_image.fill(color)
        if self.image != self.original_image:
            self.image.fill(color)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def original_width(self):
        return self.original_image.get_size()[0]

    @property
    def original_height(self):
        return self.original_image.get_size()[1]

    def set_alpha(self, alpha):        
        self.original_image.set_alpha(alpha)
        if self.original_image != self.image:
            self.image.set_alpha(alpha)

    def draw(self, surface, x, y):
        if self._width <= 0 or self._height <= 0:
            return

        surface.blit(self.image, (x, y))

    def transform(self, hotspot_x, hotpsot_y, angle, width, height):
        # implement other paramaters
        self._width = width
        self._height = height
        if self._width > 0 and self._height > 0:
            self.image = pygame.transform.smoothscale(
                self.original_image, (int(width), int(height)))

    def copy(self):
        return Texture(self.image)

    @classmethod
    def load_from_filesystem(cls, filepath):
        surface = pygame.image.load(filepath)
        surface.convert()
        return cls(surface)
