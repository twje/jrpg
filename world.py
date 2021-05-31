import math
from item_db import items_db
from core import Context
from core.graphics import SpriteFont


class Item:
    def __init__(self, idz, count):
        self.id = idz
        self.count = count


class World:
    def __init__(self):
        self.time = 0
        self.gold = 0
        # all items
        self.items = []
        # items related to quests
        self.key_items = []
        self.icons = Context.instance().data["icons"]

    # --------------
    # Public Methods
    # --------------
    def update(self, dt):
        self.time = self.time + dt

    def time_as_string(self):
        hours = math.floor(self.time/3600)
        minutes = math.floor((self.time % 3600)/60)
        seconds = self.time % 60

        return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    def gold_as_string(self):
        return str(self.gold)

    def is_item_key(self, item_id):
        return item_id in items_db and items_db[item_id]["type"] == "key"

    def add_item(self, item_id, count=1):
        assert not self.is_item_key(item_id)

        for item in self.items.items():
            if item.id == item_id:
                item.count += count
                return
        else:
            self.items.append(Item(item_id, count))

    def remove_item(self, item_id, amount=1):
        assert not self.is_item_key(item_id)

        for item in self.items.items():
            if item.id == item_id:
                item.count -= amount
                if item.count == 0:
                    self.items.remove(item)
                    return

    def has_keyz(self, item_id):
        for item in self.key_items:
            if item.id == item_id:
                return True
        return False

    def add_key(self, item_id):
        assert not self.has_keyz(item_id)
        self.key_items.append(Item(item_id, 1))

    def remove_key(self, item_id):
        for item in self.key_items.items():
            if item.id == item_id:
                self.key_items.remove(item)
        assert(False)  # never reach

    # ----------------
    # Callback Methods
    # ----------------
    def render_item(self, renderer, font, scale, x, y, item):
        if item is None:
            self.render_text(renderer, font, scale, " - ", x, y)
        else:
            items_def = items_db[item.id]
            self.render_item_slot(
                renderer,
                font,
                scale,
                x,
                y,
                items_def["name"],
                self.lookup_icon(items_def)
            )

    def render_key_item(self, renderer, font, scale, x, y, item):
        if item is None:
            self.render_text(renderer, font, scale, " - ", x, y)
        else:
            items_def = items_db[item.id]
            self.render_item_slot(
                renderer,
                font,
                scale,
                x,
                y,
                items_def["name"],
                self.lookup_icon(items_def)
            )

    # --------------
    # Helper Methods
    # --------------
    def render_item_slot(self, renderer, font, scale, x, y, text, icon):
        text_offset = self.render_icon(
            renderer,
            icon,
            scale,
            x,
            y
        )
        self.render_text(
            renderer,
            font,
            scale,
            text,
            x + text_offset,
            y
        )

    def render_text(self, renderer, font, scale, text, x, y):
        sprite = SpriteFont(text, font=font)
        sprite.set_position(x, y)
        sprite.scale_by_ratio(scale, scale)
        renderer.draw(sprite)

    def render_icon(self, renderer, icon, scale, x, y):
        text_offset = 0
        if icon:
            icon.scale_by_ratio(scale, scale)
            icon.set_position(x, y)
            text_offset += icon.width + 5
            renderer.draw(icon)

        return text_offset

    def lookup_icon(self, items_def):
        return self.icons.try_get(items_def["type"])
