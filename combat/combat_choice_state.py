from graphics.UI import Icons
from core.graphics import Sprite
from graphics.UI import Selection
from utils import lookup_texture_filepath


class CombatStateChoice:
    def __init__(self, context, actor):
        self.stack = context.stack
        self.combat_state = context
        self.actor = actor
        self.character = context.actor_char_map[actor]
        self.Icons = Icons()
        self.up_arrow = self.icons.try_get("uparrow")
        self.down_arrow = self.icons.try_get("downarrow")
        self.marker = Sprite.load_from_filesystem(
            lookup_texture_filepath(
                self.state.combat_def["continue_caret.png"]
            )
        )
        self.marker_pos = self.character.entity.get_selected_position()
        self.time = 0
        self.selection = Selection({
            "data": self.actor.actions,
            "columns": 1,
            "display_rows": 3,
            "spacing_x": 0,
            "spacing_y": 19,
            "rows": len(self.state.actors["party"]),
            "on_selection": self.on_select,
            "render_item": self.render_action,
        })

    def on_select(self, index, item):
        pass

    def render_action(sself, renderer, font, scale, x, y, item):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, renderer):
        pass