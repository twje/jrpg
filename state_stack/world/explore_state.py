import pygame
import math
from core import Context
from character import Character
from state_stack.menu import InGameMenuState
from core.system import SystemEvent

class ExploreState:
    def __init__(self, stack, camera, map, tile_x, tile_y, layer):                  
        context = Context.instance()
        self.input_manager = context.input_manager
        self.stack = stack
        self.camera = camera        
        self.event_dispatcher = context.event_dispatcher

        # hero
        self.map = map
        self.hero = Character.create_from_id("hero", self.map)
        self.hero.entity.set_tile_pos(tile_x, tile_y, layer, self.map)
        self.go_to_tile(tile_x, tile_y)
        self.__show_hero = True

        # camera
        self.follow_cam = True
        self.follow_char = self.hero
        self.manual_cam_x = 0
        self.manual_cam_y = 0                        

    # state machine methods
    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.on_use_action()
            if event.key == pygame.K_LALT:
                self.stack.push(InGameMenuState(self.stack))

    def update(self, dt):        
        self.update_audio()
        self.update_controllers(dt)
        self.update_camera()
        self.update_player_input()

    def update_audio(self):        
        if self.is_on_top():
            self.event_dispatcher.notify(SystemEvent.PLAY_MUSIC, {
                "audio_id": self.map.audio_id,                
            })        

    def update_player_input(self):
        if self.is_on_top():
            self.input_manager.add_label("move")
        else:
            self.input_manager.remove_label("move")

    def is_on_top(self):
        if self.stack is None:
            return False
        
        return self.stack.is_on_top(self)

    def update_controllers(self, dt):
        # prevent player interaction in cutscenes
        if self.__show_hero:
            self.hero.controller.update(dt)

        for npc in self.map.npcs:
            npc.controller.update(dt)

    def update_camera(self):
        if self.follow_cam:
            self.track_character()
        else:
            self.camera.set_position(
                self.manual_cam_x,
                self.manual_cam_y
            )

            # referenced by storyboard event
            self.map.cam_x = self.manual_cam_x
            self.map.cam_y = self.manual_cam_y

    def track_character(self):
        self.centre_camera_on_entity(self.follow_char.entity)

    def set_follow_cam(self, flag, character=None):
        self.follow_cam = flag
        self.follow_char = self.hero if character is None else character

        if not self.follow_cam:
            x, y = self.centre_camera_on_entity(self.follow_char.entity)
            self.manual_cam_x = x
            self.manual_cam_y = y

    def centre_camera_on_entity(self, entity):
        x, y = self.map.get_world_coord_centre(
            math.floor(entity.sprite.x),
            math.floor(entity.sprite.y)
        )
        self.camera.set_position(x, y)

        # referenced by storyboard event
        self.map.cam_x = x
        self.map.cam_y = y

        return x, y

    def render(self, renderer):
        self.render_world(renderer)

    def render_world(self, renderer):
        renderer.begin(self.camera.view)
        for layer in range(self.map.layer_count()):

            hero_entity = None
            if layer == self.hero.entity.layer:
                hero_entity = self.hero.entity

            self.map.render_layer(renderer, layer, hero_entity)
        renderer.end()

    def on_use_action(self):
        x, y = self.hero.get_faced_tile_coords()
        trigger = self.map.get_trigger(self.hero.entity.layer, x, y)
        if trigger is not None:
            trigger.on_use(
                trigger,
                self.hero.entity,
                self.hero.entity.layer,
                x,
                y,
            )

    def go_to_tile(self, tile_x, tile_y):
        x, y = self.map.get_tile_centre(tile_x, tile_y)
        self.camera.set_position(x, y)

    def hide_hero(self):
        self.hero.entity.set_tile_pos(
            self.hero.entity.tile_x,
            self.hero.entity.tile_y,
            -1,
            self.map
        )
        self.__show_hero = False

    def show_hero(self):
        self.hero.entity.set_tile_pos(
            self.hero.entity.tile_x,
            self.hero.entity.tile_y,
            0,
            self.map
        )
        self.__show_hero = True
