from graphics.UI import Textbox
from graphics.UI import Selection
import utils


class StateStack:
    def __init__(self):
        self.states = []

    def handle_input(self, event):
        top = self.top()
        if top is None:
            return

        top.handle_input(event)

    def update(self, dt):
        for state in reversed(self.states):
            update_prior_state = state.update(dt)
            if not update_prior_state:
                break

    def render(self, renderer):
        for state in self.states:
            state.render(renderer)

    def top(self):
        try:
            return self.states[-1]
        except IndexError:
            return

    def is_on_top(self, state):
        return self.top() == state

    def __len__(self):
        return len(self.states)

    def remove_top(self):
        self.states = self.states[:-1]

    def push(self, state):
        self.states.append(state)
        state.enter()

    def pop(self):
        top = self.top()
        self.remove_top()
        top.exit()
        return top

    def push_fitted(self, x, y, text_font, text, wrap=None,
                    title_font=None, title=None, avatar=None,
                    choices=None, on_finish=None):

        from core.graphics import Sprite
        from core.graphics import SpriteFont

        size = 3
        padding = size

        column_width = [[0], [0]]
        height = padding * 2

        # title
        if title:
            font_sprite = SpriteFont(title, font=title_font)
            column_width[1].append(font_sprite.width + padding)
            height += font_sprite.height

        # body text
        sprite_text = SpriteFont(
            utils.TextProcessor(
                text_font,
                text,
                wrap,
                -1,
                -1).compute_wrap()[0],
            text_font
        )
        column_width[1].append(sprite_text.width + padding * 4)
        height += sprite_text.height + padding * 2

        # selection menu
        selection_menu = None
        if choices:
            selection_menu = Selection({
                "data": choices["options"],
                "on_selection": choices["on_selection"],
            })
            column_width[1].append(selection_menu.width + padding)
            height += padding + selection_menu.height

        # append avatar child
        if avatar:
            sprite = Sprite.load_from_filesystem(avatar)
            column_width[0].append(sprite.width + padding * 3)
            height = max(height, sprite.height + padding * 4)

        width = max(column_width[0]) + max(column_width[1])
        self.push_fixed(
            x - width/2,
            y - height/2,
            width,
            height,
            text_font,
            text,
            title_font,
            title,
            avatar,
            choices,
            on_finish
        )

    def push_fixed(self, x, y, width, height, text_font, text,
                   title_font=None, title=None, avatar=None,
                   choices=None, on_finish=None):

        from core.graphics import Sprite
        from core.graphics import SpriteFont

        size = 3
        padding = size
        bounds_left = padding * 2
        bounds_top = padding * 2
        bounds_bottom = padding
        bounds_height = 0
        wrap = width - padding * 4
        children = []

        # append avatar child
        if avatar:
            sprite = Sprite.load_from_filesystem(avatar)
            bounds_left = sprite.width + padding * 3
            wrap = width - bounds_left - padding
            children.append({
                "type": "sprite",
                "sprite": sprite,
                "x": padding * 2,
                "y": padding * 2
            })

        # append title child
        if title:
            font_sprite = SpriteFont(title, font=title_font)
            bounds_top = font_sprite.height + padding * 3
            bounds_height = height - (bounds_top - bounds_bottom)
            children.append({
                "type": "text",
                "text": font_sprite,
                "x": 0,
                "y": -(font_sprite.height + padding)
            })

        # selection menu
        selection_menu = None
        if choices:
            selection_menu = Selection({
                "data": choices["options"],
                "on_selection": choices["on_selection"],
            })
            bounds_bottom += padding

        # caret
        caret = Sprite.load_from_filesystem(
            utils.lookup_texture_filepath("continue_caret.png")
        )
        carat_wiggle_room = 10
        carat_bounds_height = bounds_height - \
            (caret.height + carat_wiggle_room)

        # chunks
        bounds_height = height - (bounds_top - bounds_bottom)
        chunks = utils.TextProcessor(
            text_font,
            text, wrap, carat_bounds_height, bounds_height).compute_chunks()

        textbox_def = {
            "stack": self,
            "caret": caret,
            "carat_wiggle_room": carat_wiggle_room,
            "font": text_font,
            "chunks": chunks,
            "wrap": wrap,
            "selection_menu": selection_menu,
            "size": dict(
                left=x,
                right=x+width,
                top=y,
                bottom=y+height,
            ),
            "bounds": dict(
                left=bounds_left,
                right=-padding,
                top=bounds_top,
                bottom=-padding,
            ),
            "panel_args": dict(
                texture="gradient_panel.png",
                size=size
            ),
            "children": children,
        }
        if on_finish is not None:
            textbox_def["on_finish"] = on_finish

        self.states.append(Textbox(textbox_def))
