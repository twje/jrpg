from pathlib import Path


def navigate_up_dir(filepath, count=1):
    for _ in range(count):
        filepath = filepath.parent
    return filepath


ROOT = navigate_up_dir(Path(__file__).expanduser().resolve(), 2)

CONFIG = ROOT.joinpath("config")

LUA_SETTINGS = CONFIG.joinpath("settings.lua")
LUA_MANIFEST = CONFIG.joinpath("manifest.lua")
JSON_SETTINGS = CONFIG.joinpath("settings.json")
JSON_MANIFEST = CONFIG.joinpath("manifest.json")
JSON_DEFAULT_MANIFEST = CONFIG.joinpath("default_manifest.json")

MAPS_DIR = ROOT.joinpath("art", "maps", "data")
ASSET_DIR = ROOT
FFMPEG = ROOT.joinpath("tools", "ffmpeg.exe")