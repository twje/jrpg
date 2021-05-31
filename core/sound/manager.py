import pygame


class SoundManager:
    def __init__(self):
        self.resolver = lambda filepath: filepath
        self.library = {}

    def get_sound(self, resource_id):
        if not self.is_loaded(resource_id):
            self.library[resource_id] = self.load(resource_id)
        return self.library[resource_id]

    def is_loaded(self, resource_id):
        return resource_id in self.library

    def load(self, resource_id):
        return pygame.mixer.Sound(
            self.resolver(resource_id)
        )
