import pygame
from .widget import Widget
from core.graphics.sprite_font import Font

# scale
# fix spacing_x, spacing_t
class SelectionBuilder:
    def __init__(self):
        self.product = Selection()

    def data_model(self, data, columns=1, rows=None, display_rows=None):
        # mandatory
        self.product.menu = SelectionMenu(data, columns, rows, display_rows)
        return self

    def cursor(self, cursor):
        # mandatory
        self.product.cursor = cursor
        return self

    def layout(self, spacing_x, spacing_y):
        # optional
        self.product.spacing_x = spacing_x
        self.product.spacing_y = spacing_y
        return self

    def font(self, font):
        # optional
        self.product.font = font
        return self

    def on_select_callback(self, callback):
        # optional
        self.product.on_selection = callback
        return self

    def item_view(self, item_view):
        # optional
        self.product.item_view = item_view
        return self

    def add_border(self):
        # optional
        return self

    def position(self, x, y):
        self.product.x = x
        self.product.y = y

    def build(self):
        return self.product


class Selection(Widget):
    def __init__(self):
        self.menu = None
        self.font = Font()
        self.spacing_x = 0
        self.spacing_y = 0
        self.on_selection = None
        self.item_view = DefaultItemView
        self.cursor = None
        self.scale = 1
        self.x = 0
        self.y = 0
        self.cursor_visible = True

    def width(self):
        if self.menu.columns == 1:
            max_entry_width = 0
            for item in self.menu.data:
                item_view = self.inflate_item_view(item)
                max_entry_width = max(item_view.width(), max_entry_width)
            return max_entry_width + self.cursor.width
        else:
            return self.spacing_x * self.menu.columns

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

    def render(self, renderer):
        for i, j, x, y, item_index in self.iterate_items():
            # render cursor
            if self.is_cursor_on_item(i, j):
                self.cursor.set_position(x, y + self.cursor_offset())
                renderer.draw(self.cursor)

            item = self.get_item(item_index)
            item_view = self.inflate_item_view(item, x, y)
            item_view.render(renderer)

    # ----------
    # Client API
    # ----------
    def get_index(self):
        return self.menu.get_index()

    def get_item(self, index=None):
        return self.menu.get_item(index)

    def show_cursor(self):
        self.cursor_visible = True

    def hide_cursor(self):
        self.cursor_visible = False

    # --------------
    # Helper Methods
    # --------------
    def inflate_item_view(self, item, x=0, y=0):
        return self.item_view(self.font, self.scale, x + self.cursor.width, y, item)

    def cursor_offset(self):
        row_height = self.spacing_y * self.scale
        cursor_height = self.cursor.height
        return row_height/2 - cursor_height

    def is_cursor_on_item(self, i, j):
        if not self.cursor_visible:
            return False
        return i == self.menu.focus_y and j == self.menu.focus_x

    def iterate_items(self):
        display_start = self.menu.display_start
        display_end = display_start + self.menu.display_rows

        x = self.x
        y = self.y

        spacing_x = self.spacing_x * self.scale
        row_height = self.spacing_y * self.scale

        item_index = display_start * self.menu.columns
        for i in range(display_start, display_end):
            for j in range(0, self.menu.columns):
                yield (i, j, x, y, item_index)

                x += spacing_x
                item_index += 1
            y += row_height
            x = self.x


class SelectionMenu:
    def __init__(self, data, columns=1, rows=None, display_rows=None):
        self.data = data
        self.columns = columns
        self.max_rows = len(data) if rows is None else rows
        self.display_rows = self.max_rows if display_rows is None else display_rows
        self.display_start = 0
        self.focus_x = 0
        self.focus_y = 0

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

    def move_display_down(self):
        self.display_start += 1

    def move_display_up(self):
        self.display_start -= 1

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


class DefaultItemView:
    def __init__(self, font, scale, x, y, item):
        self.font = font
        self.scale = scale
        self.x = x
        self.y = y
        self.item = item

    def render(self, renderer):
        pass

    def width(self):
        return self.font.width(self.item)

    def height(self):
        return self.font.height()
