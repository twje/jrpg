from copy import copy


class View:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @classmethod
    def create_view_from_surface(cls, surface):
        return cls(
            0,
            0,
            surface.get_width(),
            surface.get_height(),
        )

    def copy(self):
        return copy(self)

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def __repr__(self):
        return f"l: {self.left}, t: {self.top}, r: {self.right}, b: {self.bottom}"
