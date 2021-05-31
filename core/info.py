class Info:
    def __init__(self, surface):
        self.surface = surface

    @property
    def screen_width(self):
        return self.surface.get_width()

    @property
    def screen_height(self):
        return self.surface.get_height()

    # compatibility with formmatter
    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    @property
    def x(self):
        return 0

    @property
    def y(self):
        return 0
