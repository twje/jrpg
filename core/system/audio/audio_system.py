from pygame.constants import NOEVENT
from core.system import SystemEvent
import pygame


class NullSound:
    def play(self, *args, **kwargs):
        pass


class AudioSystem:
    null_sound = NullSound()

    def __init__(self):
        self.playing = []
        self.sounds = {}
        self.music = None

    def on_notify(self, event, data):
        if event == SystemEvent.PLAY_SOUND:
            sound = self.get_sound(data["audio_id"])
            sound.play()
        elif event == SystemEvent.PLAY_MUSIC:
            audio_id = data["audio_id"]
            del data["audio_id"]
            if self.music == audio_id:
                if pygame.mixer.music.get_busy():
                    return
                pygame.mixer.music.play(**data)
            else:
                self.load_music(audio_id)
                pygame.mixer.music.play(**data)
                self.music = audio_id

    def get_sound(self, audio_id):
        if audio_id not in self.sounds:
            if not self.load_sound(audio_id):
                return self.null_sound
        return self.sounds[audio_id]

    def load_sound(self, audio_id):
        from utils import lookup_sound_filepath
        filepath = lookup_sound_filepath(audio_id)
        if filepath is None:
            return False
        self.sounds[audio_id] = pygame.mixer.Sound(filepath)            
        return True

    def load_music(self, audio_id):
        from utils import lookup_music_filepath
        pygame.mixer.music.load(lookup_music_filepath(audio_id))
