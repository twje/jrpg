from core.system.input import Binding
from core.system.input import KeyDownAction
from core.system.input import KeyPressedAction
import pygame


def create_binding(input_manager, name, action):
    binding = Binding()
    binding.add_action(action)
    input_manager.add_binding(name, binding)


def init(input_manager):
    # player controls
    create_binding(input_manager, "move_left", KeyDownAction(pygame.K_LEFT))
    create_binding(input_manager, "move_right", KeyDownAction(pygame.K_RIGHT))
    create_binding(input_manager, "move_up", KeyDownAction(pygame.K_UP))
    create_binding(input_manager, "move_down", KeyDownAction(pygame.K_DOWN))
    create_binding(input_manager, "on_use", KeyPressedAction(pygame.K_SPACE))

    # zoom camera
    create_binding(input_manager, "zoom_in", KeyDownAction(pygame.K_1))
    create_binding(input_manager, "zoom_out", KeyDownAction(pygame.K_2))

    # pan camera
    create_binding(input_manager, "pan_left", KeyDownAction(pygame.K_a))
    create_binding(input_manager, "pan_right", KeyDownAction(pygame.K_d))
    create_binding(input_manager, "pan_up", KeyDownAction(pygame.K_w))
    create_binding(input_manager, "pan_down", KeyDownAction(pygame.K_s))
