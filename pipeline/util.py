import json
from pathlib import Path
from slpp import slpp as lua


# Utility Methods
def normalize_list(value):
    if value is None:
        value = []
    if type(value) is not list:
        value = [value]

    return value


# ---------------
# Lua Descriptors
# ---------------
class LuaFilepath:
    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def new_filepath(self):
        return self.filepath.with_suffix(".json")

    def read(self):
        with open(self.filepath) as fp:
            return fp.read()


# ---------
# Modifiers
# ---------
class EnvelopWithBracketsPreModifier:
    def modify(self, contents):
        return "{ " + contents + " }"


class RemoveKeysFromSettings:
    def __init__(self):
        self.keys = (
            "main_script",
            "on_update",
            "webserver",
            "manifest"
        )

    def modify(self, contents):
        for key in self.keys:
            if key in contents:
                del contents[key]

        return contents


class ExtendManifest:
    def __init__(self, filepath):
        with open(filepath) as fp:
            self.data = json.load(fp)

    def modify(self, contents):      
        for category, entries in self.data["manifest"].items():
            for entry, asset in entries.items():                
                contents["manifest"].setdefault(category, {})[entry] = asset
        
        return contents


class RemoveLuaEncoding:
    def modify(self, contents):
        for layer in contents["layers"]:
            del layer["encoding"]
        return contents


class UpdateTilesetImageFilepath:
    def modify(self, contents):
        for tileset in contents["tilesets"]:
            filepath = Path(tileset["image"])
            filename = filepath.name
            tileset["image"] = f"../../{filename}"
        return contents


# -----
# Logic
# -----
class LuaToJsonConverter:
    def __init__(self, descriptor, pre_modifiers=None, post_modifiers=None):
        self.descriptor = descriptor
        self.pre_modifiers = normalize_list(pre_modifiers)
        self.post_modifiers = normalize_list(post_modifiers)

    def process(self):
        contents = self.descriptor.read()

        # process
        contents = self.pre_modify(contents)
        contents = lua.decode(contents)
        contents = self.post_modify(contents)

        self.serialize(contents)

    def serialize(self, contents):
        with open(self.descriptor.new_filepath, 'w') as fp:
            fp.write(json.dumps(contents, indent=4, sort_keys=True))

    def pre_modify(self, contents):
        return self.modify(contents, self.pre_modifiers)

    def post_modify(self, contents):
        return self.modify(contents, self.post_modifiers)

    @staticmethod
    def modify(value, modifiers):
        result = value
        for modifier in modifiers:
            result = modifier.modify(result)

        return result


def map_entry_collector(map_dir):
    result = []
    for entry in map_dir.iterdir():
        if entry.is_file():
            if entry.suffix != ".lua":
                continue

            result.append(
                LuaToJsonConverter(
                    descriptor=LuaFilepath(entry),
                    post_modifiers=[
                        RemoveLuaEncoding(),
                        UpdateTilesetImageFilepath()
                    ]
                )
            )
    return result


def convert_lua_to_json(dir):
    entries = [
        LuaToJsonConverter(
            descriptor=LuaFilepath(dir.LUA_MANIFEST),
            pre_modifiers=[EnvelopWithBracketsPreModifier()],
            post_modifiers=[ExtendManifest(dir.JSON_DEFAULT_MANIFEST)]
        ),
        LuaToJsonConverter(
            descriptor=LuaFilepath(dir.LUA_SETTINGS),
            pre_modifiers=[EnvelopWithBracketsPreModifier()],
            post_modifiers=[RemoveKeysFromSettings()]
        )
    ]
    entries.extend(map_entry_collector(dir.MAPS_DIR))

    for entry in entries:
        entry.process()
