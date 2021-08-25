import pygame
from core.window import Window
from core.context import Context
from core.system.render import BatchRenderer
from core.system.input import InputManager
from core.info import Info
from core import config
from core.sound import SoundManager
from core.system.audio import AudioSystem


class Application:
    def __init__(self, caption, width, height):
        # config
        settings = config.load_settings()

        # window
        self.window = Window(
            (settings["width"], settings["height"]),
            settings["name"]
        )
        self.window.event_callback = self.handle_event

        # loop
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0

        # init shared context
        self.context = Context.instance()
        self.context.input_manager = InputManager()
        self.context.sound_manager = SoundManager()
        self.context.info = Info(self.window.window_surface)
        self.context.renderer = BatchRenderer(self.window.window_surface)        

        # add listening systems
        event_dispatcher = self.context.event_dispatcher
        event_dispatcher.subscribe(AudioSystem())

        self.load()

    # --------------
    # Public Methods
    # --------------
    def run(self):
        while not self.window.is_done:
            self.handle_input()
            self.update()
            self.draw()
            self.restart_clock()

        self.destroy()

    # --------------
    # Helper Methods
    # --------------
    def handle_input(self):
        self.handle_input_hook()

    def handle_event(self, event):
        self.context.input_manager.update(event)
        self.handle_event_hook(event)

    def update(self):
        self.context.delta_time = self.elapsed_time
        self.window.update()
        self.update_hook(self.elapsed_time)
        self.context.input_manager.clear()

    def draw(self):
        self.window.begin_draw()
        self.draw_hook(self.context.renderer)
        self.window.end_draw()

    def destroy(self):
        self.window.destroy()

    def restart_clock(self):
        self.elapsed_time = self.clock.tick(60)/1000

    def store_in_context(self, key, value):
        self.context.data[key] = value
        return value

    # -----
    # Hooks
    # -----
    def load(self):
        pass

    def handle_input_hook(self):
        pass

    def handle_event_hook(self, event):
        pass

    def update_hook(self):
        pass

    def draw_hook(self, renderer):
        pass
