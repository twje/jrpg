from anim_entity_fx import AnimEntityFx
from core import Context
from storyboard.storyboard import Storyboard
from storyboard import events


class CEUseItem:
    def __init__(self, state, owner, item_def, targets):
        conext = Context.instance()
        self.entity_defs = conext.data["entity_definitions"]
        self.world = conext.data["world"]
        self.state = state
        self.owner = owner
        self.item_def = item_def
        self.targets = targets
        self.character = state.actor_char_map[owner]
        self.name = f"{owner.name} using {item_def['name']}"
        self.done = False

        self.controller = self.character.controller
        self.controller.change("cs_run_anim", {"anim": "prone"})

        self.storyboard = Storyboard(
            self.state.stack, [
                events.function(self.show_item_notice),
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "use", "loop": False}),
                events.function(self.do_use_item),
                events.wait(2),  # time to read notice
                events.run_state(self.controller, "cs_move", {"dir": -1}),
                events.function(self.do_finish)
            ])

        # item is exhausted - remove from inventory
        self.world.remove_item(item_def["id"])

    def time_points(self, queue):
        speed = self.owner.stats.get("speed")
        return queue.speed_to_time_points(speed)

    def show_item_notice(self):
        self.state.show_notice(f"Item: {self.item_def['name']}")

    def do_use_item(self):
        self.state.hide_notice()
        position = self.character.entity.get_selected_position()
        entity_def = self.entity_defs.get_entity_def("fx_use_item")
        effect = AnimEntityFx(
            position[0],
            position[1],
            entity_def,
            entity_def["frames"],
        )
        self.state.add_effect(effect)
        
        self.run_item_action()        

    def run_item_action(self):
        action = self.item_def["use"]["action"]

    def do_finish(self):
        self.done = True

    def execute(self, queue):
        self.state.stack.push(self.storyboard)

    def is_finished(self):
        return self.done

    def update(self):
        pass
