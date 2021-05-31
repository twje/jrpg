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
