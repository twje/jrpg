from core.graphics import TextureAtlas
from core.graphics import Sprite


class ScrollBar:
    def __init__(self, texture_filepath, tile_height, height=None):
        self.x = 0
        self.y = 0
        self.height = 300 if height is None else height
        self.caret_size = 1
        self.value = 0

        self.tile_height = tile_height
        atlas = TextureAtlas.load_from_filepath(
            texture_filepath,
            tile_height=self.tile_height
        )
        self.sprite_up = Sprite(atlas[0].copy())
        self.sprite_caret = Sprite(atlas[1].copy())
        self.sprite_background = Sprite(atlas[2].copy())
        self.sprite_down = Sprite(atlas[3].copy())

        self.tile_width = self.sprite_up.width
        self.line_height = self.height - self.tile_height * 2  # ignore arrows

        self.set_position(self.x, self.y)

    @property
    def width(self):
        return self.tile_width

    def set_position(self, x, y):
        self.x = x
        self.y = y

        # up
        self.sprite_up.set_position(self.x, self.y)

        # background
        self.sprite_background.set_position(x, self.y + self.tile_height)
        self.sprite_background.scale_by_ratio(
            1,
            self.line_height/self.tile_height
        )

        # down
        self.sprite_down.set_position(
            self.x,
            self.y + self.tile_height + self.line_height
        )

        self.set_normal(self.value)

    def set_scroll_caret_scale(self, normal_value):
        self.caret_size = (self.line_height * normal_value)/self.tile_height

    def set_normal(self, value):
        self.value = value
        self.sprite_caret.scale_by_ratio(1, self.caret_size)
        room = self.line_height - self.sprite_caret.height
        start = self.y + self.tile_height + room * self.value
        self.sprite_caret.set_position(self.x, start)

    def render(self, renderer):
        renderer.draw(self.sprite_up)
        renderer.draw(self.sprite_background)
        renderer.draw(self.sprite_caret)
        renderer.draw(self.sprite_down)
