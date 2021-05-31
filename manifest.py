class Manifest:
    def __init__(self, manifest):
        self.manifest = manifest["manifest"]

    def get_texture_filepath(self, resource_id):
        if resource_id in self.manifest["textures"]:
            return self.manifest["textures"][resource_id]["path"]
        return resource_id

    def get_font_filepath(self, resource_id):
        if resource_id in self.manifest["fonts"]:
            return self.manifest["fonts"][resource_id]["path"]
        return resource_id

    def get_map_filepath(self, resource_id):
        if resource_id in self.manifest["maps"]:
            return self.manifest["maps"][resource_id]["path"]
        return resource_id

    def get_sound_filepath(self, resource_id):
        if resource_id in self.manifest["sounds"]:
            return self.manifest["sounds"][resource_id]["path"]
        return resource_id
