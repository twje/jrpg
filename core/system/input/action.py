from .base import InputAction
import pygame


class KeyPressedAction(InputAction):
    def __init__(self, key):
        self.key = key
        self.satisfied = False

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.key:
                self.satisfied = True

    def clear(self):
        self.satisfied = False


class KeyDownAction(InputAction):
    def __init__(self, key):
        self.key = key

    @property
    def satisfied(self):
        return pygame.key.get_pressed()[self.key]


class DelayedKeyDownAction(InputAction):
    def __init__(self, key):
        self.key = key
        self.start_time = pygame.time.get_ticks()
        self.delay_time = 100
        self.is_clear = True

    @property
    def satisfied(self):
        # reset
        is_pressed = pygame.key.get_pressed()[self.key]
        if not is_pressed:
            self.is_clear = True
            return False

        # update
        elapsed = pygame.time.get_ticks()
        if self.is_clear:
            self.start_time = elapsed
            self.is_clear = False
            return True
        else:
            if elapsed - self.start_time > self.delay_time:
                self.start_time = elapsed
                return True

        return False
