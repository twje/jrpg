from . import Texture
from . import Sprite
import pygame


def draw_rect(renderer, x, y, width, height, color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)
    texture = Texture(surface)
    sprite = Sprite(texture)
    sprite.set_position(x, y)
    renderer.draw(sprite)
