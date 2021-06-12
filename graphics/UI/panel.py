from core.graphics.texture_atlas import TextureAtlas
from core.graphics.sprite import Sprite


class Panel:
    def __init__(self, texture_atlas, tile_size):
        self.tiles = {}
        self.tile_size = tile_size

        # create a sprite for each tile of the panel
        # 0. top left      1. top          2. top right
        # 3. left          4. middle       5. right
        # 6. bottom left   7. bottom       8. bottom right
        for index in range(9):
            sprite = Sprite(texture_atlas[index])
            self.tiles[index] = sprite

    def position(self, left, top, right, bottom):
        # normalize
        if left > right:
            left, right = right, left
        if top > bottom:
            top, bottom = bottom, top

        # lengths
        width = abs(right - left) - self.tile_size * 2
        height = abs(bottom - top) - self.tile_size * 2

        # center tile
        self.tiles[4].set_position(left + self.tile_size, top + self.tile_size)
        self.tiles[4].scale_by_size(width, height)

        # left tile
        self.tiles[3].set_position(left, top + self.tile_size)
        self.tiles[3].scale_by_size(self.tile_size, height)

        # top tile
        self.tiles[1].set_position(left + self.tile_size, top)
        self.tiles[1].scale_by_size(width, self.tile_size)

        # right tile
        self.tiles[5].set_position(
            right - self.tile_size, top + self.tile_size)
        self.tiles[5].scale_by_size(self.tile_size, height)

        # bottom
        self.tiles[7].set_position(
            left + self.tile_size, bottom - self.tile_size)
        self.tiles[7].scale_by_size(width, self.tile_size)

        # align corner tiles
        self.tiles[0].set_position(left, top)
        self.tiles[2].set_position(right - self.tile_size, top)
        self.tiles[6].set_position(left, bottom - self.tile_size)
        self.tiles[8].set_position(
            right - self.tile_size, bottom - self.tile_size)

        # hide corner tiles when size is equal to zero
        if left - right == 0 or top - bottom == 0:
            for tile in self.tiles.values():
                tile.scale_by_size(0, 0)

    def center_position(self, x, y, width, height):
        h_width = width/2
        h_height = height/2
        self.position(x - h_width, y - h_height, x + h_width, y + h_height)

    def relative_position(self, x, y, width, height):
        self.position(x, y, x + width, y + height)

    def render(self, renderer):
        for index in range(9):
            renderer.draw(self.tiles[index])

    @classmethod
    def load_from_texture(cls, texture_filepath, size):
        texture_atlas = TextureAtlas.load_from_filepath(
            texture_filepath,
            size,
            size
        )
        return cls(texture_atlas, size)


class EnvelopePanel:
    def __init__(self, subject, texture_filepath, size, padding):
        self.subject = subject
        self.panel = Panel.load_from_texture(texture_filepath, size)
        self.padding = padding

    def render(self, renderer):
        self.panel.position(
            self.subject.x - self.padding,
            self.subject.y - self.padding,
            self.subject.x + self.subject.width + self.padding,
            self.subject.y + self.subject.height + self.padding
        )
        self.panel.render(renderer)
