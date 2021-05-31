from .buffer import Buffer
from .view import View


class BatchRenderer:
    def __init__(self, window_surface):
        self.window_surface = window_surface
        self.buffer = Buffer()

        self.default_view = View.create_view_from_surface(self.window_surface)
        self.view = None

    def begin(self, view=None):
        if view is None:
            view = self.default_view
        self.view = view

        self.buffer.sync(view.width, view.height)

    def draw(self, renderable):
        # convert world to screen coordinates
        offset_x = -self.view.x
        offset_y = -self.view.y

        renderable.draw(self.buffer.surface, offset_x, offset_y)

    def end(self):
        self.buffer.flush(self.window_surface)
        self.buffer.clear((0, 0, 0, 0))
