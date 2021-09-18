from anim_entity_fx import AnimEntityFx
from core import Context
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.combat_target_state import CombatSelector
from combat import combat_formula
from item_db import items_db


class CESteal:
    def __init__(self, state, owner, special_def, targets):
        context = Context.instance()
        self.entity_defs = context.data["entity_definitions"]
        self.world = context.data["world"]
        self.state = state
        self.owner = owner
        self.special_def = special_def
        self.targets = targets
        self.name = f"Steal for {owner.name}"
        self.character = state.actor_char_map[owner]
        self.entity = self.character.entity
        self.default_targeter = CombatSelector.weakest_enemy
        self.controller = self.character.controller
        self.done = False

        self.original_pos = None  # self.entity.sprite.get_position()
        self.storyboard = Storyboard(
            self.state.stack, [
                events.function(self.show_notice),
                events.wait(0.2),
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.function(self.store_position),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "steal_1", "loop": False}),
                events.function(self.teleport_out),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "steal_2", "loop": False}),
                events.wait(1.1),
                events.function(self.do_steal),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "steal_3", "loop": False}),
                events.function(self.teleport_in),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "steal_4", "loop": False}),
                events.function(self.show_result),
                events.wait(1.0),
                events.function(self.hide_notice),
                events.run_state(self.controller, "cs_move", {"dir": -1}),
                events.wait(0.2),
                events.function(self.on_finish),
            ])

    def store_position(self):
        self.original_pos = self.entity.sprite.get_position()

    def do_steal(self):
        target = self.targets[0]
        self.state.hide_notice()

        if target.steal_item is None:
            self.state.show_notice("Nothing to steal.")
            return

        success = self.steal_from(target)

        if success:
            item_id = target.steal_item
            item_def = items_db[item_id]
            name = item_def["name"]
            self.world.add_item(item_id)
            target.steal_item = None
            self.state.show_notice(f"Stolon: {name}")
        else:
            self.state.show_notice("Steal failed.")

    def steal_from(self, target):
        success = combat_formula.steal(self.owner, target)
        target_entity = self.state.actor_char_map[target].entity
        target_position = target_entity.sprite.get_position()

        entity_def = self.entity_defs.get_entity_def("slash")
        effect = AnimEntityFx(
            target_position[0],
            target_position[1],
            entity_def,
            entity_def["frames"],
        )
        self.state.add_effect(effect)

        return success

    def teleport_out(self):
        target = self.targets[0]
        target_entity = self.state.actor_char_map[target].entity
        target_pos_x, target_pos_y = target_entity.sprite.get_position()

        subject_entity = self.character.entity
        subject_entity.sprite.set_position(
            target_pos_x - subject_entity.width/2, target_pos_y)

    def teleport_in(self):
        self.entity.sprite.set_position(*self.original_pos)

    def show_result(self):
        pass

    def show_notice(self):
        self.state.show_notice(self.special_def["name"])

    def hide_notice(self):
        self.state.hide_notice()

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

    def notice(self, text):
        self.state.show_notice(text)

    def on_finish(self):
        self.done = True

    def execute(self, queue):
        pass

    def update(self):
        self.state.stack.push(self.storyboard)
        self.remove_dead_enemies_as_targets()

    def remove_dead_enemies_as_targets(self):
        for target in list(self.targets):
            hp = target.stats.get("hp_now")
            is_enemy = not self.state.is_party_member(target)
            if is_enemy and hp <= 0:
                self.targets.remove(target)

        if len(self.targets) == 0:
            self.targets = self.default_targeter(self.state)

    def is_finished(self):
        return self.done
