from collections import defaultdict
import json
import math


# fix imports
from core.graphics import SpriteAtlas
from core.graphics import Sprite
from core.graphics.texture_atlas import TextureAtlas
from core import Context
from trigger import Trigger
from actions import action_registry
import utils


def load_tiled_map_from_filesystem(map_filepath, map_seed_filepath=None):
    # load map
    with open(map_filepath) as fp:
        map_def = json.load(fp)

    # seed map with entities
    if map_seed_filepath is not None:
        with open(map_seed_filepath) as fp:
            map_def.update(json.load(fp))

    return TiledMap(map_def)


class TiledMap:
    def __init__(self, map_def):
        self.map_def = map_def

        self.context = Context.instance()
        self.renderer = self.context.renderer

        self.layer = self.map_def["layers"][0]
        self.width = self.layer["width"]
        self.height = self.layer["height"]

        self.tiles = self.layer["data"]
        self.tile_width = self.map_def["tilesets"][0]["tilewidth"]
        self.tile_height = self.map_def["tilesets"][0]["tileheight"]

        self.width_pixel = self.width * self.tile_width
        self.height_pixel = self.height * self.tile_height
        self.debug = True

        self.tile_sprite = SpriteAtlas(
            TextureAtlas.load_from_filepath(
                # hack
                filepath=utils.lookup_texture_filepath(
                    utils.strip_filepath(
                        self.map_def["tilesets"][0]["image"]
                    )
                ),
                tile_width=self.tile_width,
                tile_height=self.tile_height
            )
        )
        self.blocking_tile = self.parse_blocking_tile_id()

        # query trigger per layer, tile index
        self.triggers, self.trigger_types = self.load_triggers()

        # query entity per layer, tile index
        self.entities = defaultdict(dict)

        # iterate all npcs
        self.npcs = []
        self.npc_by_id = {}

        self.on_wake()

    def write_tile(self, x, y, layer, tile, detail=0, is_collision=False):
        layer = layer * 3
        collision = self.blocking_tile
        if is_collision is None:
            collision = 0
        index = self.coord_to_index(x, y)

        # tile
        tiles = self.map_def["layers"][layer]["data"]
        tiles[index] = tile

        # detail
        tiles = self.map_def["layers"][layer + 1]["data"]
        tiles[index] = detail

        # collision
        tiles = self.map_def["layers"][layer + 2]["data"]
        tiles[index] = collision

    def remove_trigger(self, x, y, layer=0):
        triggers = self.triggers[layer]
        index = self.coord_to_index(x, y)
        del triggers[index]

    def add_trigger(self, x, y, layer, trigger_type):
        triggers = self.triggers[layer]
        trigger = self.trigger_types[trigger_type]
        triggers[self.coord_to_index(x, y)] = trigger

    def on_wake(self):
        for action_def in self.map_def.get("on_wake", []):
            action = action_registry[action_def["id"]]
            params = action_def["params"]

            # remove common params - check for defaults
            params, location = utils.extract_from_dict(
                params, ["tile_x", "tile_y"], {"layer": 0}
            )
            action(self, **params)(None, None, **location)

    def extract_from_dict(self, store, mandatory_keys, optional_keys):
        # extract mandatory key
        result = {k: store[k] for k in mandatory_keys}
        for k in mandatory_keys:
            del store[k]

        # extract optional keys
        result.update(
            {k: store.get(k, optional_keys[k]) for k in optional_keys}
        )
        for k in optional_keys:
            if k in store:
                del store[k]

        return result

    def load_triggers(self):
        self.debug = self.map_def.get("debug", False)
        actions = self.parse_actions()
        trigger_types = self.parse_trigger_types(actions)
        triggers = self.place_triggers(trigger_types)

        return triggers, trigger_types

    def parse_actions(self):
        actions = {}
        for action_def in self.map_def.get("actions", []):
            for action_def_id, params in action_def.items():
                action_id = params["id"]
                params = params["params"]
                actions[action_def_id] = action_registry[action_id](
                    self, **params)

        return actions

    def parse_trigger_types(self, actions):
        trigger_types = {}
        for trigger_def in self.map_def.get("trigger_types", []):
            for trigger_def_id, callbacks in trigger_def.items():
                # update callback with action
                for key, action_def_id in callbacks.copy().items():
                    callbacks[key] = actions[action_def_id]

                trigger_types[trigger_def_id] = Trigger(callbacks)

        return trigger_types

    def place_triggers(self, trigger_types):
        triggers = defaultdict(dict)
        for trigger in self.map_def.get("triggers", []):
            layer = trigger.get("layer", 0)
            index = self.coord_to_index(
                trigger["tile_x"],
                trigger["tile_y"]
            )
            triggers[layer][index] = trigger_types[trigger["trigger"]]

        return triggers

    def parse_blocking_tile_id(self):
        for tileset in self.map_def["tilesets"]:
            if tileset["name"] == "collision_graphic":
                # -1 because tiled starts at 1 (offset)
                blocking_tile = tileset["firstgid"] - 1
                break
        else:
            raise Exception("collision tile not detected")

        return blocking_tile

    def remove_entity(self, entity):
        # add assert - page 142
        entities = self.entities[entity.layer]
        index = self.coord_to_index(entity.tile_x, entity.tile_y)
        del entities[index]

    def add_entity(self, entity):
        # add assert - page 142
        entities = self.entities[entity.layer]
        index = self.coord_to_index(entity.tile_x, entity.tile_y)
        entities[index] = entity

    def get_entity(self, tile_x, tile_y, layer):
        # add assert - page 142
        entities = self.entities[layer]
        index = self.coord_to_index(tile_x, tile_y)
        return entities.get(index)

    def add_npc(self, npc):
        self.npcs.append(npc)

    def get_npc(self, tile_x, tile_y, layer):
        for npc in self.npcs:
            if (npc.entity.tile_x == tile_x
                and npc.entity.tile_y == tile_y
                    and npc.entity.layer == layer):

                return npc

    def remove_npc(self, tile_x, tile_y, layer):
        for index, npc in enumerate(self.npcs):
            if (npc.entity.tile_x == tile_x
                and npc.entity.tile_y == tile_y
                    and npc.entity.layer == layer):

                self.remove_entity(npc.entity)
                del self.npcs[index]
                del self.npc_by_id[npc.id]

                return True
        return False

    def render_layer(self, renderer, layer, hero):
        tile_left, tile_top = self.point_to_tile(
            self.renderer.view.left,
            self.renderer.view.top
        )

        tile_right, tile_bottom = self.point_to_tile(
            self.renderer.view.right,
            self.renderer.view.bottom
        )

        layer_index = layer * 3

        # render tiles
        rows = range(tile_top, tile_bottom + 1)
        cols = range(tile_left, tile_right + 1)
        for j_tile in rows:
            for i_tile in cols:
                # position tile
                self.tile_sprite.set_position(
                    i_tile * self.tile_width,
                    j_tile * self.tile_height,
                )

                # base layer
                tile = self.get_tile_index(i_tile, j_tile, layer_index)
                if tile >= 0:  # -1 is nothing
                    self.tile_sprite.update_texture(tile)
                    renderer.draw(self.tile_sprite)

                # decoration layer
                tile = self.get_tile_index(i_tile, j_tile, layer_index + 1)
                if tile >= 0:  # -1 is nothing
                    self.tile_sprite.update_texture(tile)
                    renderer.draw(self.tile_sprite)

                # render debug
                # check layer is correct for layer > 0 - todo
                self.render_debug(renderer, layer, i_tile, j_tile)

        # render entities
        entity_layer = self.entities[layer]
        draw_list = []
        if hero is not None:
            draw_list.append(hero)

        for _, entity in entity_layer.items():
            draw_list.append(entity)

        draw_list.sort(key=lambda entity: entity.tile_y)
        for entity in draw_list:
            entity.render(renderer)

    def render_debug(self, renderer, layer, tile_x, tile_y):
        if not self.debug:
            return

        trigger = self.get_trigger(layer, tile_x, tile_y)
        if trigger is None:
            return

        # tile
        x, y = self.get_tile_coord(tile_x, tile_y)
        color = (255, 0, 0, 70)
        overlay = Sprite.create_rectangle(
            x, y, 100, 100, color
        )
        renderer.draw(overlay)

    def get_trigger(self, layer, x, y):
        try:
            triggers = self.triggers[layer]
        except IndexError:
            return

        index = self.coord_to_index(x, y)
        return triggers.get(index)

    def layer_count(self):
        # layer is made up of 3 sections
        return int(len(self.map_def["layers"]) / 3)

    def get_tile_index(self, x, y, layer=0):
        tiles = self.map_def["layers"][layer]["data"]
        return tiles[self.coord_to_index(x, y)] - 1

    def coord_to_index(self, x, y):
        return x + y * self.width

    def is_blocked(self, layer, tile_x, tile_y):
        # collision layer is 2 above offical layer
        tile = self.get_tile_index(tile_x, tile_y, layer + 2)
        entity = self.get_entity(tile_x, tile_y, layer)

        return tile == self.blocking_tile or entity is not None

    def point_to_tile(self, x, y):
        # clamp point to bounds of map
        x = max(0, x)
        y = max(0, y)
        x = min(self.width_pixel - 1, x)
        y = min(self.height_pixel - 1, y)

        # map from bounded point to tile
        tile_x = math.floor(x / self.tile_width)
        tile_y = math.floor(y / self.tile_height)

        return tile_x, tile_y

    def get_tile_centre(self, tile_x, tile_y):
        "<update>"
        screen_width = self.context.info.screen_width
        screen_height = self.context.info.screen_height
        x = tile_x * self.tile_width - (screen_width + self.tile_width)/2
        y = tile_y * self.tile_height - (screen_height + self.tile_height)/2

        return x, y

    def get_world_coord_centre(self, world_x, world_y):
        "<update>"
        screen_width = self.context.info.screen_width
        screen_height = self.context.info.screen_height
        x = world_x - (screen_width + self.tile_width)/2
        y = world_y - (screen_height + self.tile_height)/2

        return x, y

    def get_tile_foot(self, tile_x, tile_y):
        "get tile foot to offset sprites"
        x = tile_x * self.tile_width
        y = tile_y * self.tile_height + self.tile_height
        return x, y

    def get_tile_coord(self, tile_x, tile_y):
        "get tile foot to offset sprites"
        x = tile_x * self.tile_width
        y = tile_y * self.tile_height
        return x, y
