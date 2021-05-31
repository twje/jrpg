from core.graphics import Texture
from core.graphics import Sprite
from core.tween import Tween
from core import Context
import pygame


class FadeState:
    def __init__(self, stack, start=1, finish=0, duration=1, color=(0, 0, 0)):
        self.stack = stack
        self.start = start
        self.finish = finish
        self.duration = duration
        self.color = color
        self.tween = Tween(self.start, self.finish, self.duration)
        self.square = type(self).new_surface(self.color)

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        self.tween.update(dt)
        alpha = int(255 * self.tween.value)
        self.square.set_alpha(alpha)

        if self.tween.is_finished:
            self.stack.pop()

        return True

    def render(self, renderer):
        renderer.draw(self.square)

    @staticmethod
    def new_surface(color):
        context = Context.instance()
        surface = pygame.Surface(
            (
                context.info.screen_width,
                context.info.screen_height
            ), pygame.SRCALPHA
        )
        surface.fill(color)

        return Sprite(Texture(surface))
