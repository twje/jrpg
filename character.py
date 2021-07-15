from collections import namedtuple
from core import Context
from entity import Entity
from state_machine import StateMachine
from state_machine import state_registry


# switch out maps for storyboard replace_scene
class MapRef:
    def __init__(self, map):
        self.map = map


class Character:
    def __init__(self, character_def, map):
        self.id = None
        self.map_ref = MapRef(map)
        self.entity = type(self).create_entity(character_def)
        self.actor_id = character_def.get("actor_id")
        self.facing = character_def.get("facing")
        self.anims = character_def.get("anims", {})
        self.path = None
        self.path_index = -1
        self.talk_index = 0
        self.controller = self.create_controller(character_def)
        self.default_state = character_def["state"]
        self.prv_default_state = self.default_state
        self.controller.change(self.default_state)

    def reset_map(self, map):
        self.map_ref.map = map

    def get_faced_tile_coords(self):
        x_inc = 0
        y_inc = 0
        if self.facing == "left":
            x_inc = -1
        elif self.facing == "right":
            x_inc = 1
        elif self.facing == "up":
            y_inc = -1
        elif self.facing == "down":
            y_inc = 1

        x = self.entity.tile_x + x_inc
        y = self.entity.tile_y + y_inc

        return x, y

    def follow_path(self, path):
        self.path_index = 0
        self.path = path
        self.default_state = "follow_path"
        self.controller.change("follow_path")

    def is_path_complete(self):
        return self.path_index >= len(self.path)

    def is_path_exhausted(self):
        return any((
            self.path_index == -1,
            self.is_path_complete()
        ))

    def path_direction(self):
        return self.path[self.path_index]

    def increment_path(self):
        self.path_index += 1

    def reset_default_state(self):
        self.default_state = self.prv_default_state

    def get_combat_anim(self, id):
        if id in self.anims:
            return self.anims[id]
        else:
            return self.entity.start_frame

    @classmethod
    def create_from_id(cls, chracter_id, map):
        context = Context.instance()
        entity_defs = context.data["entity_definitions"]
        character_def = entity_defs.get_character_def(chracter_id)

        return cls(character_def, map)

    # --------------
    # Helper Methods
    # --------------
    @staticmethod
    def create_entity(character_def):
        return Entity.create_from_id(character_def["entity"])

    def create_controller(self, character_def):
        controller = StateMachine()
        controller.set_states({
            key: self.state_factory(state_registry[key]) for
            key in character_def["controller"]
        })

        return controller

    def state_factory(self, state):
        return lambda: state(self, self.map_ref.map)
