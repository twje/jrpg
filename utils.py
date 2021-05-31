import copy
from pathlib import Path
from core import Context


def strip_filepath(filepath):
    return Path(filepath).name


def lookup_texture_filepath(resource_id):
    context = Context.instance()
    manifest = context.data["manifest"]
    return manifest.get_texture_filepath(resource_id)


def lookup_font_filepath(resource_id):
    context = Context.instance()
    manifest = context.data["manifest"]
    return manifest.get_font_filepath(resource_id)


def lookup_sound_filepath(resource_id):
    context = Context.instance()
    manifest = context.data["manifest"]
    return manifest.get_sound_filepath(resource_id)


def extract_from_dict(store, mandatory_keys, optional_keys):
    """
    Extract subset of keys from a dictionary
    """
    # preserve original dictionary
    store = copy.deepcopy(store)

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

    return store, result


def ternary_not(value1, value2):
    return value1 if value1 is not None else value2


class TextProcessor:
    def __init__(self, font, text, wrap, intermediate_height, final_height):
        self.font = font
        self.text = text
        self.wrap = wrap
        self.intermediate_height = intermediate_height
        self.final_height = final_height
        self.chunk = []
        self.chunks = []

    # ---
    # API
    # ---
    def compute_chunks(self):
        start, finish = self.wrap_text(0)
        current_height = self.font.height()

        self.new_chunk(start, finish)
        while finish < len(self.text):
            start, finish = self.wrap_text(finish)

            if self.is_overflow(current_height, self.is_last_chunk(finish)):
                self.new_chunk(start, finish)
                current_height = 0
            else:
                self.append_chunk(start, finish)

            current_height += self.font.height()

        return self.chunks

    def compute_wrap(self):
        start, finish = self.wrap_text(0)

        self.new_chunk(start, finish)
        while finish < len(self.text):
            start, finish = self.wrap_text(finish)
            self.append_chunk(start, finish)

        return self.chunks

    # --------------
    # Helper Methods
    # --------------
    def wrap_text(self, start):
        finish = start
        while self.within_width(start, finish):
            finish += 1

        # edge case - fix
        if start == 0 and finish == len(self.text):
            return start, finish + 1

        last_finish = self.text.rfind(" ", 0, finish)

        if last_finish < 0:
            self.hyphonate(finish)
        else:
            start, finish = self.wrap_index(start, finish)

        return start, finish

    def is_last_chunk(self, finish):
        return finish >= len(self.text)

    def is_overflow(self, current_height, is_last_chunk):
        total_height = current_height + self.font.height()
        if is_last_chunk:
            return total_height > self.final_height
        else:
            return total_height > self.intermediate_height

    def new_chunk(self, start, finish):
        self.chunk = [self.text[start:finish]]
        self.chunks.append(self.chunk)

    def append_chunk(self, start, finish):
        self.chunk.append(self.text[start:finish])

    def within_width(self, start, finish):
        return self.font.width(self.text[start:finish]) < self.wrap and \
            (finish < len(self.text))

    def wrap_index(self, start, finish):
        # first character of first chunk is not a space
        space_ignore_index = 0 if start == 0 else 1

        if finish < len(self.text):
            last_index = self.text.rfind(" ", start, finish)
            if last_index >= 0:
                return start + space_ignore_index, last_index
        return start, finish

    def hyphonate(self, index):
        self.text = self.text[:index - 1] + '-' + self.text[index - 1:]
