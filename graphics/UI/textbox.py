from collections import namedtuple
import math
import pygame
from core import tween
from core.graphics import SpriteFont
from graphics.UI import Panel
import utils

Rect = namedtuple("Rect", "left top, right, bottom")


class Textbox:
    def __init__(self, textbox_def):
        # back panel
        self.panel = Panel.load_from_texture(
            utils.lookup_texture_filepath(
                textbox_def["panel_args"]["texture"]
            ),
            textbox_def["panel_args"]["size"],
        )

        # attributes
        self.stack = textbox_def["stack"]
        self.caret = textbox_def["caret"]
        self.carat_wiggle_room = textbox_def["carat_wiggle_room"]
        self.chunks = textbox_def["chunks"]
        self.font = textbox_def["font"]
        self.wrap = textbox_def.get("wrap")
        self.size = Rect(**textbox_def["size"])
        self.bounds = Rect(**textbox_def["bounds"])
        self.children = textbox_def.get("children", [])
        self.selection_menu = textbox_def["selection_menu"]
        self.on_finish = textbox_def.get("on_finish", lambda: None)
        self.appear_tween = tween.Tween(0, 1, 0.5, tween.ease_out_circ)
        self.x = self.size.left + (self.size.right - self.size.left) / 2
        self.y = self.size.top + (self.size.bottom - self.size.top) / 2
        self.width = self.size.right - self.size.left
        self.height = self.size.bottom - self.size.top
        self.chunk_index = 0
        self.time = 0
        self.do_click_callback = False

        # body text
        self.body_text = SpriteFont(
            self.chunks[0],
            self.font
        )

    def enter(self):
        pass

    def exit(self):
        if self.do_click_callback:
            self.selection_menu.on_click()
        self.on_finish()

    def update(self, dt):
        self.time += dt
        self.appear_tween.update(dt)
        if self.is_dead():
            self.stack.pop()

        return True

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.on_click()
            elif self.selection_menu:
                self.selection_menu.handle_input(event)

    def on_click(self):
        if self.selection_menu:
            self.do_click_callback = True

        if self.chunk_index + 1 >= len(self.chunks):
            # ignore when during animation
            if not self.appear_tween.is_finished or self.appear_tween.value == 0:
                return
            self.appear_tween = tween.Tween(1, 0, 0.3, tween.ease_in_circ)
        else:
            self.chunk_index += 1
            if self.chunk_index < len(self.chunks):
                self.body_text = SpriteFont(
                    self.chunks[self.chunk_index],
                    self.font
                )

    def is_dead(self):
        return self.appear_tween.is_finished and self.appear_tween.value == 0

    def render(self, renderer):
        renderer.begin()

        scale = self.appear_tween.value

        # panel
        self.panel.center_position(
            self.x,
            self.y,
            self.width * scale,
            self.height * scale
        )
        self.panel.render(renderer)

        # position text in bounds
        left = self.x - (self.width/2 * scale)
        text_left = left + (self.bounds.left * scale)
        top = self.y - (self.height/2 * scale)
        text_top = top + (self.bounds.top * scale)
        bottom = self.y + (self.height/2 * scale)
        caret_bottom = bottom + \
            (self.bounds.bottom - self.caret.height) * scale

        # body text
        self.body_text.set_position(text_left, text_top)
        self.body_text.scale_by_ratio(scale, scale)
        renderer.draw(self.body_text)

        # selection menu
        if self.selection_menu:
            menu_x = text_left
            menu_y = bottom - self.selection_menu.height
            self.selection_menu.set_position(menu_x, menu_y)
            self.selection_menu.scale = scale
            self.selection_menu.render(renderer)

        # continue mark
        if self.chunk_index + 1 < len(self.chunks):
            animate = self.carat_wiggle_room * math.sin(self.time * 10)/2
            offset = caret_bottom - \
                (self.carat_wiggle_room + animate) * scale / 2
            self.caret.set_position(self.x, offset)
            self.caret.scale_by_ratio(scale, scale)
            renderer.draw(self.caret)

        # children
        for child in self.children:
            if child["type"] == "text":
                font_sprite = child["text"]
                font_sprite.set_position(
                    text_left + (child["x"] * scale),
                    text_top + (child["y"] * scale)
                )
                font_sprite.scale_by_ratio(scale, scale)
                renderer.draw(font_sprite)
            elif child["type"] == "sprite":
                sprite = child["sprite"]
                sprite.set_position(
                    left + (child["x"] * scale),
                    top + (child["y"] * scale)
                )
                sprite.scale_by_ratio(scale, scale)
                renderer.draw(sprite)

        renderer.end()
