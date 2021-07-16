
import copy
from utils import lookup_texture_filepath
from state_stack import StateStack
from core.graphics import Sprite
from core import Context
from character import Character
from dependency import Injector
from dependency import Payload


class CombatState(Injector):
    # 0 - 1, each number is a percentage of with, hegiht offset from center of the screen
    LAYOUT = {
        "party": [
            [
                (0.25, -0.056, 0, 0)
            ],
            [
                (0.23, 0.024, 0, 0),
                (0.27, -0.136, 0, 0),
            ],
            [
                (0.73, 0.364, 0, 0),
                (0.75, 0.444, 0, 0),
                (0.77, 0.524, 0, 0),
            ]
        ],
        "enemy": [
            [
                (0.25, 0.56, 0, 0),
            ],
            [
                (-0.23, 0.024, 0, 0),
                (-0.27, -0.136, 0, 0),
            ],
            [
                (-0.21, -0.056, 0, 0),
                (-0.23, 0.024, 0, 0),
                (-0.27, -0.136, 0, 0),
            ],
            [
                (-0.18, -0.056, 0, 0),
                (-0.23, 0.056, 0, 0),
                (-0.25, -0.056, 0, 0),
                (-0.27, -0.168, 0, 0),
            ],
            [
                (-0.28, 0.032, 0, 0),
                (-0.3, -0.056, 0, 0),
                (-0.32, -0.144, 0, 0),
                (-0.2, 0.004, 0, 0),
                (-0.24, -0.116, 0, 0),
            ],
            [
                (-0.28, 0.032, 0, 0),
                (-0.3, -0.056, 0, 0),
                (-0.32, -0.144, 0, 0),
                (-0.16, 0.032, 0, 0),
                (-0.205, -0.056, 0, 0),
                (-0.225, -0.144, 0, 0),
            ]
        ]
    }

    def __init__(self, stack, combat_def):
        super().__init__()
        Character.register_as_dependency_injector(self)

        self.game_stack = stack
        self.combat_def = combat_def
        self.stack = StateStack()
        self.context = Context.instance()
        self.entity_defs = self.context.data["entity_definitions"]
        self.info = self.context.info
        self.actors = {
            "party": self.combat_def["actors"]["party"],
            "enemy": self.combat_def["actors"]["enemy"],
        }
        self.characters = {
            "party": [],
            "enemy": []
        }
        self.select_actor = None
        self.actor_char_map = {}

        # UI components
        self.background = Sprite.load_from_filesystem(
            lookup_texture_filepath(self.combat_def["background"])
        )
        self.init_ui()

        self.create_combat_characters("party")
        self.create_combat_characters("enemy")

    def get_dependency(self, identifier):
        if identifier == "combat_scene":
            return Payload(self)

    def init_ui(self):        
        self.background.scale_by_size(self.info.screen_width, self.info.screen_height)

    def create_combat_characters(self, side):
        actor_list = self.actors[side]
        character_list = self.characters[side]
        layout = self.LAYOUT[side][len(actor_list) - 1]
        for index, actor in enumerate(actor_list):
            char_def = copy.copy(self.entity_defs.get_character_def(actor.id))

            # override with combat entity
            if "combat_entity" in char_def:
                char_def["entity"] = char_def["combat_entity"]

            character = Character(char_def, None)
            character_list.append(character)
            
            self.actor_char_map[actor] = character            
            position = layout[index]

            x = position[0] * self.info.screen_width
            y = position[1] * self.info.screen_height
            character.entity.sprite.set_position(x, y)

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, dt):
        return False

    def render(self, renderer):
        renderer.begin()
        renderer.draw(self.background)
        for character in self.characters['party']:
            character.entity.render(renderer)
        for character in self.characters['enemy']:
            character.entity.render(renderer)
        renderer.end()
