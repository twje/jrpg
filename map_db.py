import json
from graphics.tiled_map import load_tiled_map_from_filesystem


class MapDB:
    def __init__(self, filepath):
        with open(filepath) as fp:
            self.data = json.load(fp)

    def new_map(self, map_id, map_seed_id=None):
        return load_tiled_map_from_filesystem(
            self.filepath(map_id),
            self.seed_filepath(map_seed_id)
        )

    def filepath(self, map_id):
        return self.data["maps"][map_id]["data"]

    def seed_filepath(self, map_seed_id):
        if map_seed_id is None:
            return
        return self.data["seeds"][map_seed_id]["data"]
