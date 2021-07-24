from core.graphics import Sprite
from core.graphics import Font
from core.graphics import SpriteFont
import utils as game_utils
from core.graphics import util as graphics_util
import pygame


class Selection:
    def __init__(self, select_def):
        self.x = select_def.get("x", 0)
        self.y = select_def.get("y", 0)
        self.data = select_def["data"]
        self.columns = select_def.get("columns", 1)
        self.focus_x = 0
        self.focus_y = 0
        self.spacing_x = select_def.get("spacing_x", 128)
        self.spacing_y = select_def.get("spacing_y", 24)
        self.cursor = None
        self._show_cursor = True,
        self.max_rows = select_def.get("rows", len(self.data))
        self.display_start = 0
        self.scale = 1
        self.font = select_def.get("font", Font())
        self.on_selection = select_def.get(
            "on_selection", lambda index, item: None)
        self.display_rows = select_def.get("display_rows", self.max_rows)
        self.cursor = Sprite.load_from_filesystem(
            game_utils.lookup_texture_filepath("cursor.png")
        )
        self.render_item = select_def.get(
            "render_item", self.default_render_item)
        self.calc_item_width = select_def.get("calc_item_width")
        self._width = self.calc_width()
        self._height = self.calc_height()
        self.debug = False

    @property
    def width(self):
        return self._width * self.scale

    @property
    def height(self):
        return self._height * self.scale

    def calc_width(self):
        if self.columns == 1:
            max_entry_width = 0
            for item in self.data:
                if self.calc_item_width:
                    width = self.calc_item_width(self.font, item)
                else:
                    width = self.font.width(str(item))
                max_entry_width = max(width, max_entry_width)
            return max_entry_width + self.cursor.width
        else:
            return self.spacing_x * self.columns

    def cursor_width(self):
        return self.cursor.width

    def align_hort(self, x):
        self.x = x - self.cursor.width

    def calc_height(self):
        return self.display_rows * self.spacing_y

    def show_cursor(self):
        self._show_cursor = True

    def hide_cursor(self):
        self._show_cursor = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def can_scroll_up(self):
        return self.display_start > 0

    def can_scroll_down(self):
        return self.display_start < (self.max_rows - self.display_rows)

    def percentage_scrolled(self):
        one_percent = 1 / self.max_rows
        current_percent = self.focus_y / self.max_rows

        if current_percent <= one_percent:
            current_percent = 0
        return current_percent

    def selected_item(self):
        try:
            return self.data[self.get_index()]
        except IndexError:
            return None

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_up()
            elif event.key == pygame.K_DOWN:
                self.move_down()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_SPACE:
                self.on_click()

    def move_up(self):
        self.focus_y = max(self.focus_y - 1, 0)
        if self.focus_y < self.display_start:
            self.move_display_up()

    def move_down(self):
        self.focus_y = min(self.focus_y + 1, self.max_rows - 1)
        if self.focus_y >= self.display_start + self.display_rows:
            self.move_display_down()

    def move_right(self):
        self.focus_x = min(self.focus_x + 1, self.columns - 1)

    def move_left(self):
        self.focus_x = max(self.focus_x - 1, 0)

    def on_click(self):
        index = self.get_index()
        self.on_selection(index, self.get_item(index))

    def get_index(self):
        return self.focus_x + self.focus_y * self.columns

    def get_item(self, index=None):
        try:
            if index is None:
                item = self.data[self.get_index()]
            else:
                item = self.data[index]
        except IndexError:
            item = None
        return item

    def move_display_down(self):
        self.display_start += 1

    def move_display_up(self):
        self.display_start -= 1

    def render(self, renderer):
        if self.debug:
            self.debug_render(renderer)

        self.cursor.scale_by_ratio(self.scale, self.scale)

        for i, j, x, y, item_index in self.iterate_items():
            # render cursor
            if self.is_cursor_on_item(i, j):
                self.cursor.set_position(x, y + self.cursor_offset())
                renderer.draw(self.cursor)

            # render item
            item = self.get_item(item_index)
            self.render_item(renderer, self.font, self.scale, x +
                             self.cursor.width, y, item)

    def cursor_offset(self):
        row_height = self.spacing_y * self.scale
        cursor_height = self.cursor.height
        return row_height/2 - cursor_height

    def iterate_items(self):
        display_start = self.display_start
        display_end = display_start + self.display_rows

        x = self.x
        y = self.y

        spacing_x = self.spacing_x * self.scale
        row_height = self.spacing_y * self.scale

        item_index = display_start * self.columns
        for i in range(display_start, display_end):
            for j in range(0, self.columns):
                yield (i, j, x, y, item_index)

                x += spacing_x
                item_index += 1
            y += row_height
            x = self.x

    def default_render_item(self, renderer, font, scale, x, y, item):
        if item is None:
            font_sprite = SpriteFont("--", font=font)
        else:
            font_sprite = SpriteFont(item, font=font)

        font_sprite.set_position(x, y)
        font_sprite.scale_by_ratio(scale, scale)
        renderer.draw(font_sprite)

    def debug_render(self, renderer):
        graphics_util.draw_rect(
            renderer,
            self.x,
            self.y,
            self.width,
            self.height,
            (255, 0, 255)
        )

    def is_cursor_on_item(self, i, j):
        if not self._show_cursor:
            return False

        return i == self.focus_y and j == self.focus_x
