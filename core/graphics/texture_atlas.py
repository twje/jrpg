# from pathlib import Path
from core.graphics.texture import Texture
import pygame


class TextureAtlas:
    def __init__(self, surface, tile_width, tile_height):
        self.surface = surface
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.textures = []

        cols = int(surface.get_width() / tile_width)
        rows = int(surface.get_height() / tile_height)

        for j in range(rows):
            for i in range(cols):
                rect = pygame.Rect(
                    i * tile_width,
                    j * tile_height,
                    tile_width,
                    tile_height
                )
                image = pygame.Surface(rect.size, pygame.SRCALPHA)
                image.blit(surface, (0, 0), rect)
                self.textures.append(Texture(image))

    def __getitem__(self, key):
        return self.textures[key]

    def copy(self):
        return type(self)(self.surface, self.tile_width, self.tile_height)

    @staticmethod
    def load_from_filepath(filepath, tile_width=None, tile_height=None):        
        surface = pygame.image.load(filepath)
        surface.convert()
        return TextureAtlas(
            surface,
            surface.get_width() if tile_width is None else tile_width,
            surface.get_height() if tile_height is None else tile_height
        )
