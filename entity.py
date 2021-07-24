from core.graphics import SpriteAtlas
# from loaders import load_texture_atlas_from_manifest
from core.graphics import TextureAtlas
from core import Context


class Entity:
    def __init__(self, entity_def):
        self.width = entity_def["width"]
        self.height = entity_def["height"]
        self.tile_x = entity_def.get("tile_x", 0)
        self.tile_y = entity_def.get("tile_y", 0)
        self.layer = entity_def.get("layer", 0)
        self.start_frame = entity_def["start_frame"]
        self.sprite = type(self).create_sprite_atlas(entity_def)
        self.set_frame(self.start_frame)

        # children entities
        self.children = {}
        self.x = entity_def.get("x", 0)
        self.y = entity_def.get("y", 0)

    def get_selected_position(self):        
        x_pos = self.x + self.width/2
        y_pos = self.y + self.height/2 
        y_pad = 32
        return x_pos, y_pos - y_pad

    def set_frame(self, frame):
        self.sprite.update_texture(frame)

    def set_tile_pos(self, x, y, layer, map):
        "track entities in map"
        if map.get_entity(self.tile_x, self.tile_y, self.layer) == self:
            map.remove_entity(self)

        # check target tile
        if map.get_entity(x, y, layer) is not None:
            raise Exception("Entity already occupies tiles")

        self.tile_x = x
        self.tile_y = y
        self.layer = layer

        # add to map
        map.add_entity(self)
        self.x, self.y = map.get_tile_foot(self.tile_x, self.tile_y)
        self.sprite.set_position(self.x, self.y - self.height)

    def add_child(self, child_id, entity):
        self.children[child_id] = entity

    def remove_child(self, child_id):
        del self.children[child_id]

    def render(self, renderer):
        renderer.draw(self.sprite)
        for child in self.children.values():
            child_sprite = child.sprite
            child_sprite.set_position(
                self.x + child.x,
                self.y - child.y - self.sprite.height,
            )
            renderer.draw(child_sprite)

    @classmethod
    def create_from_id(cls, entity_id):
        context = Context.instance()
        entity_defs = context.data["entity_definitions"]
        entity_def = entity_defs.get_entity_def(entity_id)

        return cls(entity_def)

    # --------------
    # Helper Methods
    # --------------
    @staticmethod
    def create_sprite_atlas(entity_def):
        manifest = Context.instance().data["manifest"]
        texture_atlas = TextureAtlas.load_from_filepath(
            filepath=manifest.get_texture_filepath(entity_def["texture"]),
            tile_width=entity_def["width"],
            tile_height=entity_def["height"]
        )
        return SpriteAtlas(texture_atlas)
