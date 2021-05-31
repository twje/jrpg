from . import utils


class Buffer:
    def __init__(self):
        self.surface = None

    def sync(self, width, height):
        if self.surface is None:
            self.surface = utils.new_surface(width, height)

        if not utils.is_surface_congruent(self.surface, width, height):
            self.surface = utils.new_surface(width, height)

    def flush(self, target_surface):
        normalized_surface = utils.resize_surface(
            self.surface,
            target_surface.get_width(),
            target_surface.get_height()
        )
        target_surface.blit(normalized_surface, (0, 0))

    def clear(self, clear_color):
        self.surface.fill(clear_color)
