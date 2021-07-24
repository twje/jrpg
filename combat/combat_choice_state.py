import math
from combat.actor import Actor
from .combat_target_state import CombatTargetState
from .combat_target_state import CombatTargetType
from core.graphics.sprite_font import Font, FontStyle
from core.graphics.sprite_font import SpriteFont
from graphics.UI import Icons
from core.graphics import Sprite
from graphics.UI import Selection
from functools import partial
from graphics.UI import create_fixed_textbox
from utils import lookup_texture_filepath


class CombatStateChoice:
    def __init__(self, context, actor):
        self.stack = context.stack
        self.combat_state = context
        self.actor = actor
        self.character = context.actor_char_map[actor]
        self.icons = Icons()
        self.up_arrow = self.icons.try_get("uparrow")
        self.down_arrow = self.icons.try_get("downarrow")
        self.marker = Sprite.load_from_filesystem(
            lookup_texture_filepath("continue_caret.png")
        )
        self.marker_pos = self.character.entity.get_selected_position()
        self.time = 0

        font = Font(FontStyle.small())
        self.textbox = create_fixed_textbox(
            self.stack,
            0,
            0,
            130,
            65,
            font,
            "",
            selection=Selection({
                "data": self.actor.actions,
                "columns": 1,
                "display_rows": 3,
                "spacing_x": 0,
                "spacing_y": 19,
                "font": font,
                "on_selection": self.on_select,
                "render_item": self.render_action,
            })
        )
        self.textbox.x = 65
        self.textbox.y = 280
        self.selection = self.textbox.selection_menu

    def set_arrow_position(self):
        pad = 20
        x_pos = self.selection.x + self.selection.width + pad

        # up arrow
        y_pos = self.selection.y
        self.up_arrow.set_position(x_pos, y_pos)

        # down arrow
        y_pos = self.selection.y + self.selection.height - self.down_arrow.height
        self.down_arrow.set_position(x_pos, y_pos)

    def on_select(self, index, data):
        print("on select", index, data)

        if data == "attack":            
            self.selection.hide_cursor()
            state = CombatTargetState(
                self.combat_state,
                target_type = CombatTargetType.SIDE,
                on_select = partial(self.take_action, data),
                on_exit = None
            )
            self.stack.push(state)            
    
    def take_action(self, action_id, targets):
        print(action_id, targets)

    def render_action(self, renderer, font, scale, x, y, item):        
        text = Actor.ACTION_LABELS.get(item, "")
        sprite = SpriteFont(text, font=font)
        sprite.scale_by_ratio(scale, scale)
        sprite.set_position(x, y)
        renderer.draw(sprite)

    def enter(self):
        self.combat_state.selected_actor = self.actor

    def exit(self):
        self.combat_state.selected_actor = None

    def handle_input(self, event):        
        self.selection.handle_input(event)

    def update(self, dt):
        self.textbox.update(dt)
        x_pos = self.marker_pos[0] - self.marker.width/2
        y_pos = self.marker_pos[1]

        self.time += dt
        self.marker.set_position(x_pos, y_pos + math.sin(self.time * 10))

        return False

    def render(self, renderer):
        self.textbox.render(renderer)
        renderer.draw(self.marker)
        self.set_arrow_position()

        # prevent showing arrows while tween in progress - hack
        if not self.textbox.is_active():
            return

        if self.selection.can_scroll_up():
            renderer.draw(self.up_arrow)

        if self.selection.can_scroll_down():
            renderer.draw(self.down_arrow)
