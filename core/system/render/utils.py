import pygame


def new_surface(width, height):
    # may need to convert - https://www.pygame.org/docs/ref/surface.html#pygame.Surface
    return pygame.Surface((width, height), pygame.SRCALPHA)


def is_surface_congruent(surface, width, height):
    return surface.get_width() == width and surface.get_height() == height


def resize_surface(surface, width, height):
    if is_surface_congruent(surface, width, height):
        return surface

    return pygame.transform.scale(surface, (width, height))
