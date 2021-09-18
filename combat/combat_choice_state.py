from os import stat
from combat.browse_list_state import BrowseListState
import math
from combat.actor import Actor
from .combat_target_state import CombatTargetState
from .combat_target_state import CombatTargetType
from .event import CEAttack
from .event import CEFlee
from .event import CEUseItem
from .event import CECastSpell
from core.graphics.sprite_font import Font, FontStyle
from core.graphics.sprite_font import SpriteFont
from graphics.UI import Icons
from core.graphics import Sprite
from graphics.UI import Selection
from functools import partial
from graphics.UI import create_fixed_textbox
from utils import lookup_texture_filepath
from core import Context
from item_db import items_db
from spell_db import spell_db


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
        self.hide = False

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
        self.textbox.y = 257
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
        if data == "attack":
            self.selection.hide_cursor()
            state = CombatTargetState(
                self.combat_state,
                target_type=CombatTargetType.ONE,
                on_select=partial(self.take_action, data),
                on_exit=None
            )
            self.stack.push(state)
        elif data == "flee":
            self.stack.pop()  # CombatStateChoice
            queue = self.combat_state.event_queue
            event = CEFlee(self.combat_state, self.actor)
            tp = event.time_points(queue)
            queue.add(event, tp)
        elif data == "item":
            self.on_item_action()
        elif data == "magic":
            self.on_magic_action()

    def on_magic_action(self):
        state = None
        self.selection.hide_cursor()

        def on_render_item(renderer, font, scale, x, y, spell_id):
            text = "--"
            cost = "0"
            canCast = False
            mp = self.actor.stats.get("mp_now")

            color = (255, 255, 255, 255)
            if spell_id is not None:
                spell_def = spell_db[spell_id]
                text = spell_def["name"]
                cost = spell_def["mp_cost"]

                canCast = mp >= cost
                if not canCast:
                    color = (178, 178, 178, 255)

                sprite = SpriteFont(str(cost), font)
                sprite.scale_by_ratio(scale, scale)
                sprite.set_position(x + 96, y)
                sprite.set_color(color)
                renderer.draw(sprite)

            sprite = SpriteFont(text, font)
            sprite.scale_by_ratio(scale, scale)
            sprite.set_position(x, y)
            sprite.set_color(color)
            renderer.draw(sprite)

        def on_exit():
            self.combat_state.hide_tip()
            self.selection.show_cursor()

        def on_selection(index, spell_id):            
            if spell_id is None:
                return
            
            spell_def = spell_db[spell_id]
            mp = self.actor.stats.get("mp_now")
            if mp < spell_def["mp_cost"]:
                return

            targeter = self.create_action_targeter(spell_def, state, CECastSpell)
            self.stack.push(targeter)

        state = BrowseListState(
            stack=self.stack,
            title="MAGIC",
            data=self.actor.magic,
            on_exit=on_exit,
            on_render_item=on_render_item,
            on_selection=on_selection,
        )
        self.stack.push(state)

    def create_action_targeter(self, spell_def, browse_state, ce_class):
        target_def = spell_def["target"]        
        browse_state.hide()
        self.hide = True

        def on_select(targets):
            self.stack.pop()  # CombatTargetState
            self.stack.pop()  # BrowseListState
            self.stack.pop()  # CombatStateChoice

            queue = self.combat_state.event_queue
            event = ce_class(
                self.combat_state,
                self.actor,
                spell_def,
                targets
            )
            tp = event.time_points(queue)
            queue.add(event, tp)            

        def on_exit():
            browse_state.show()
            self.hide = False

        return CombatTargetState(
            self.combat_state,
            select_type=target_def["type"],
            default_selector=target_def["selector"],
            can_switch_sides=target_def["switch_sides"],
            on_select=on_select,
            on_exit=on_exit
        )

    def on_item_action(self):
        state = None
        self.selection.hide_cursor()

        def on_focus(item):
            text = ""
            if item is not None:
                item_def = items_db[item.id]
                text = item_def["description"]
            self.combat_state.show_tip(text)

        def on_render_item(renderer, font, scale, x, y, item):
            text = "--"
            if item is not None:
                item_def = items_db[item.id]
                text = item_def["name"]
                if item.count > 1:
                    text = f"{text} x{item.count}"

            sprite = SpriteFont(text, font)
            sprite.scale_by_ratio(scale, scale)
            sprite.set_position(x, y)
            renderer.draw(sprite)

        def on_exit():
            self.combat_state.hide_tip()
            self.selection.show_cursor()

        def on_selection(index, item):
            if item is None:
                return
            item_def = items_db[item.id]
            targeter = self.create_item_targeter(item_def, state)
            self.stack.push(targeter)

        state = BrowseListState(
            stack=self.stack,
            title="ITEMS",
            data=self.get_useable_items(),
            on_exit=on_exit,
            on_render_item=on_render_item,
            on_focus=on_focus,
            on_selection=on_selection,
        )
        self.stack.push(state)

    def get_useable_items(self):
        world = Context.instance().data["world"]
        return world.filter_items(lambda item: item["type"] == "useable")

    def create_item_targeter(self, item_def, browse_state):
        target_def = item_def["use"]["target"]
        browse_state.hide()
        self.hide = True

        def on_select(targets):
            self.stack.pop()  # CombatTargetState
            self.stack.pop()  # BrowseListState
            self.stack.pop()  # CombatStateChoice

            queue = self.combat_state.event_queue
            event = CEUseItem(
                self.combat_state,
                self.actor,
                item_def,
                targets
            )
            tp = event.time_points(queue)
            queue.add(event, tp)

        def on_exit():
            browse_state.show()
            self.hide = False

        return CombatTargetState(
            self.combat_state,
            select_type=target_def["type"],
            default_selector=target_def["selector"],
            can_switch_sides=target_def["switch_sides"],
            on_select=on_select,
            on_exit=on_exit
        )

    def take_action(self, action_id, targets):
        self.stack.pop()  # CombatTargetState
        self.stack.pop()  # CombatStateChoice

        queue = self.combat_state.event_queue

        if action_id == "attack":
            event = CEAttack(self.combat_state, self.actor,
                             {"player": True}, targets)
            tp = event.time_points(queue)
            queue.add(event, tp)

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
        if self.hide:
            return

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
