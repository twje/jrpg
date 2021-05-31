from core.system.render import View


class Camera:
    def __init__(self, view):
        self.original_view = view
        self.view = view.copy()
        self.zoom = 1

    @classmethod
    def create_camera_from_surface(cls, surface):
        view = View(
            0,
            0,
            surface.get_width(),
            surface.get_height(),
        )
        return cls(view)

    @property
    def x(self):
        return self.view.x

    @property
    def y(self):
        return self.view.y

    def move(self, x, y):
        self.view.x += x
        self.view.y += y
        self.original_view.x += x
        self.original_view.y += y

    def set_position(self, x, y):
        self.view.x = x
        self.view.y = y
        self.original_view.x = x
        self.original_view.y = y

    def increment_zoom(self, ratio):
        self.zoom += ratio
        self.sync()

    def set_zoom(self, ratio):
        self.zoom = ratio
        self.sync()

    def sync(self):
        # calculate
        x_extend = self.view.width * (self.zoom - 1) / 2
        y_extend = self.view.height * (self.zoom - 1) / 2

        # update view
        self.view.x = self.original_view.x - x_extend
        self.view.y = self.original_view.y - y_extend
        self.view.width = self.original_view.width + 2 * x_extend
        self.view.height = self.original_view.height + 2 * y_extend
