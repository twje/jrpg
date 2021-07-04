from dataclasses import dataclass
from . import register_state
from core.system.input import InputProcessor
from combat.actor import Actor
from core import Context
from combat import ActorSummary
from graphics.menu import Layout
from graphics.UI import Icons
from core.graphics import formatter
from core.graphics import FontStyle
from core.graphics import SpriteFont
from core.graphics import Font
from graphics.UI import ScrollBar
from graphics.UI import Selection
from item_db import items_db
import utils
import pygame


@dataclass
class EventAdapter:
    type: int
    key: int


@register_state("equipment")
class EquipmentMenuState:
    def __init__(self, parent):
        # state
        context = Context.instance()
        self.parent = parent
        self.stack = parent.stack
        self.state_machine = parent.state_machine
        self.world = context.data["world"]
        self.font = Font(style=FontStyle.default())
        self.in_list = False

        # input
        self.input_namespace = "equip_menu_nav"
        self.input_manager = context.input_manager
        self.input_processor = InputProcessor(
            self.input_manager,
            self.input_namespace
        )
        self.input_processor.bind_callback("nav_move_up", self.move_cursor_up)
        self.input_processor.bind_callback(
            "nav_move_down", self.move_cursor_down)
        self.input_processor.bind_callback("on_use", self.select_option)

        # layout 1
        self.layout = Layout()
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort('screen', 'top', 'bottom', 0.12, 2)
        self.layout.split_vert('top', 'title', 'category', 0.25, 2)
        title_panel = self.layout.panels["title"]

        # layout 2
        self.layout = Layout()
        self.layout.contract("screen", 118, 40)
        self.layout.split_hort("screen", "top", "bottom", 0.42, 2)
        self.layout.split_hort("bottom", "desc", "bottom", 0.2, 2)
        self.layout.split_vert("bottom", "stats", "list", 0.4, 2)
        self.layout.panels["title"] = title_panel

        # UI components
        self.panels = [
            self.layout.create_panel("top"),
            self.layout.create_panel("desc"),
            self.layout.create_panel("stats"),
            self.layout.create_panel("list"),
            self.layout.create_panel("title"),
        ]
        self.scrollbar = ScrollBar(
            utils.lookup_texture_filepath("scrollbar.png"),
            18,
            self.layout.layout("list").height
        )
        icons = Icons()
        self.better_sprite = icons.try_get("uparrow")
        self.worse_sprite = icons.try_get("downarrow")

        self.init_ui_components()

        # set on enter
        self.actor = None
        self.actor_summary = None
        self.equipment = None
        self.menu_index = None
        self.filter_menus = None
        self.slot_menu = None

    def init_ui_components(self):
        list_layout = self.layout.layout("list")

        self.scrollbar.set_position(
            formatter.right_justify(0, list_layout, self.scrollbar),
            formatter.top_justify(0, list_layout, self.scrollbar),
        )

    def refresh_filtered_menu(self):
        filter_list = []
        slot_count = len(self.actor.active_equip_slots)

        # init filter list
        for index in range(slot_count):
            slot_type = self.actor.slot_types[index]
            filter_list.append({
                "type": slot_type,
                "list": []
            })

        # sort inventory items into lists
        for entry in self.world.items:
            item = items_db[entry.id]
            for filter in filter_list:
                # come back
                if item["type"] == filter["type"] and self.actor.can_use(item):
                    filter["list"].append(entry)

        self.filter_menus = []
        for entry in filter_list:
            menu = Selection({
                "data": entry["list"],
                "spacing_x": 256,
                "spacing_y": 28,
                "columns": 1,
                "display_rows": 5,
                "rows": 20,
                "render_item": self.world.render_item,
                "on_selection": self.on_do_equip,
                "font": self.font,
            })
            self.filter_menus.append(menu)

    def enter(self, data):
        self.input_manager.add_label(self.input_namespace)
        self.input_manager.clear()
        self.actor = data["actor"]
        self.actor_summary = ActorSummary(self.actor, {"show_xp": False})
        self.equipment = self.actor.equipment

        self.refresh_filtered_menu()
        self.menu_index = 0
        self.filter_menus[self.menu_index].hide_cursor()

        self.slot_menu = Selection({
            "data": self.actor.active_equip_slots,
            "on_selection": self.on_select_menu,
            "spacing_y": 28,
            "columns": 1,
            "rows": len(self.actor.active_equip_slots),
            "render_item": self.actor.render_equipment,
            "font": self.font,
        })

    def exit(self):
        self.input_manager.remove_label(self.input_namespace)

    def update(self, dt):
        if not self.input_processor.is_active():
            return
        self.input_processor.process()
        self.update_scrollbar()

    def update_input(self, event):
        if self.in_list:
            self.handle_filter_list_input(event)
        else:
            self.handle_slot_menu_input(event)

    def move_cursor_up(self):
        event = EventAdapter(pygame.KEYDOWN, pygame.K_UP)
        if self.in_list:
            self.handle_filter_list_input(event)
        else:
            self.handle_slot_menu_input(event)

    def move_cursor_down(self):
        event = EventAdapter(pygame.KEYDOWN, pygame.K_DOWN)
        if self.in_list:
            self.handle_filter_list_input(event)
        else:
            self.handle_slot_menu_input(event)

    def select_option(self):
        event = EventAdapter(pygame.KEYDOWN, pygame.K_SPACE)
        if self.in_list:
            self.handle_filter_list_input(event)
        else:
            self.handle_slot_menu_input(event)

    def get_selected_slot(self):
        index = self.slot_menu.get_index()
        return Actor.EQUIP_SLOT_ID[index]

    def get_selected_item(self):
        if self.in_list:
            menu = self.filter_menus[self.menu_index]
            item = menu.selected_item()
            return None if item is None else item.id
        else:
            slot = self.get_selected_slot()
            return self.actor.equipment[slot]

    def stat_difference(self):
        slot = self.get_selected_slot()
        item_id = self.get_selected_item()
        item = None
        if item_id is not None:
            item = items_db[item_id]
        return self.actor.predict_stats(slot, item)

    def on_do_equip(self, index, item):
        self.actor.equip(self.get_selected_slot(), item)
        self.refresh_filtered_menu()
        self.focus_slot_menu()

    def on_select_menu(self, index, item):
        self.in_list = True
        self.slot_menu.hide_cursor()
        self.menu_index = self.slot_menu.get_index()
        self.filter_menus[self.menu_index].show_cursor()

    def handle_input(self, event):
        if not self.in_list:
            self.handle_menu_exit(event)
        elif self.is_exit_menu_event(event):
            self.focus_slot_menu()

    def handle_filter_list_input(self, event):
        menu = self.filter_menus[self.menu_index]
        menu.handle_input(event)

    def handle_slot_menu_input(self, event):
        prev_equip_index = self.slot_menu.get_index()
        self.slot_menu.handle_input(event)
        if prev_equip_index != self.slot_menu.get_index():
            self.on_equip_menu_changed()

    def handle_menu_exit(self, event):
        if self.is_exit_menu_event(event):
            self.state_machine.change("frontmenu")

    def update_scrollbar(self):
        menu = self.filter_menus[self.menu_index]
        self.scrollbar.set_normal(menu.percentage_scrolled())

    def is_exit_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key in (
                pygame.K_ESCAPE,
                pygame.K_BACKSPACE
            )
        return False

    def is_exit_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key in (
                pygame.K_ESCAPE,
                pygame.K_BACKSPACE
            )
        return False

    def focus_slot_menu(self):
        self.in_list = False
        self.slot_menu.show_cursor()
        self.menu_index = self.slot_menu.get_index()
        self.filter_menus[self.menu_index].hide_cursor()

    def on_equip_menu_changed(self):
        # equip menu only changes, when list isn't in focus
        self.menu_index = self.slot_menu.get_index()
        self.filter_menus[self.menu_index].hide_cursor()

    def render(self, renderer):
        self.render_panels(renderer)
        self.render_title(renderer)
        self.render_character_summary(renderer)
        self.render_slot_menu(renderer)
        self.render_inventoru_menu(renderer)
        self.render_scrollbar(renderer)
        self.render_character_stats(renderer)
        self.render_description(renderer)

    def render_panels(self, renderer):
        for panel in self.panels:
            panel.render(renderer)

    def render_title(self, renderer):
        layout = self.layout.layout("title")
        sprite = SpriteFont("Items", font=self.font)
        sprite.set_position(
            formatter.center_x(layout, sprite),
            formatter.center_y(layout, sprite),
        )
        renderer.draw(sprite)

    def render_character_summary(self, renderer):
        title_height = self.layout.layout("title").height
        avatar_x = self.layout.left("top")
        avatar_y = self.layout.top("top")
        avatar_x += 10
        avatar_y += title_height + 10
        self.actor_summary.set_position(avatar_x, avatar_y)
        self.actor_summary.render(renderer)

    def render_slot_menu(self, renderer):
        title_height = self.layout.layout("title").height
        equip_x = self.layout.mid_x("top") - 30
        equip_y = self.layout.top("top") + title_height
        self.slot_menu.set_position(equip_x, equip_y)
        self.slot_menu.render(renderer)

    def render_inventoru_menu(self, renderer):
        list_x = self.layout.left("list") + 6
        list_y = self.layout.top("list") + 20
        menu = self.filter_menus[self.menu_index]
        menu.set_position(list_x, list_y)
        menu.render(renderer)

    def render_scrollbar(self, renderer):
        self.scrollbar.render(renderer)

    def render_character_stats(self, renderer):
        font = Font(FontStyle.small())
        diffs = self.stat_difference()

        stat_list = self.actor.create_stat_name_list()
        stat_labels = self.actor.create_stat_label_list()

        for index, stat in enumerate(stat_list):
            self.draw_stat(
                renderer,
                font,
                self.layout.left("stats") + 5,
                self.layout.top("stats") + (font.height() + 2) * index + 5,
                stat_labels[index],
                stat,
                diffs[stat]
            )

    def draw_stat(self, renderer, font, x, y, label, stat, diff):
        layout = self.layout.layout("stats")
        current = self.actor.stats.get(stat)
        changed = current + diff

        entries = [
            SpriteFont(f"{label}:", font),
            SpriteFont(str(current), font),
        ]

        if diff > 0:            
            entries.extend(self.add_stat_arrow(
                SpriteFont(str(changed), font),
                self.better_sprite,
                (0, 255, 0),
            ))
        elif diff < 0:
            entries.extend(self.add_stat_arrow(
                SpriteFont(str(changed), font),
                self.worse_sprite,
                (0, 255, 0),
            ))     
        else:
            for entry in entries:
                entry.set_color((255, 255, 255))

        for entry in entries:
            entry.y = y
            formatter.in_place_multi_hort(
                start=layout.x,
                margin=5,
                seperators=[100, 70, 20, 0],
                drawables=entries
            )
            renderer.draw(entry)

    def add_stat_arrow(self, stat, arrow, color):
        stat.set_color(color)        
        return [stat, arrow]

    def render_description(self, renderer):
        item_id = self.get_selected_item()
        if item_id is None:
            return
        layout = self.layout.layout("desc")
        item = items_db[item_id]
        text = SpriteFont(item["description"], Font())
        text.set_position(
            formatter.center_x(layout, text),
            formatter.center_y(layout, text),
        )
        renderer.draw(text)
