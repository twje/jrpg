
from anim_entity_fx import AnimEntityFx
from core import Context
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.combat_target_state import CombatSelector
from combat.combat_actions import combat_action_registry


class CECastSpell:
    def __init__(self, state, owner, spell_def, targets):
        conext = Context.instance()
        self.entity_defs = conext.data["entity_definitions"]
        self.state = state
        self.owner = owner
        self.spell_def = spell_def
        self.targets = targets
        self.character = state.actor_char_map[owner]
        self.name = f"{owner.name} is casting {spell_def['name']}"
        self.done = False

        self.controller = self.character.controller
        self.controller.change("cs_run_anim", {"anim": "prone"})

        self.storyboard = Storyboard(
            self.state.stack, [
                events.function(self.show_spell_notice),
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.wait(0.5),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "cast", "loop": False}),
                events.wait(0.12),
                events.no_block(
                    events.run_state(self.controller, "cs_run_anim", {
                        "anim": "prone"})
                ),
                events.function(self.do_cast),
                events.wait(1.0),
                events.function(self.hide_spell_notice),
                events.run_state(self.controller, "cs_move", {"dir": -1}),
                events.function(self.do_finish)
            ])

    def do_cast(self):
        position = self.character.entity.get_selected_position()
        entity_def = self.entity_defs.get_entity_def("fx_use_item")
        effect = AnimEntityFx(
            position[0],
            position[1],
            entity_def,
            entity_def["frames"],
        )
        self.state.add_effect(effect)

        mp = self.owner.stats.get("mp_now")
        cost = self.spell_def["mp_cost"]
        mp = max(mp - cost, 0)
        self.owner.stats.set("mp_now", mp)
        self.run_spell_action()

    def run_spell_action(self):
        action_id = self.spell_def["action"]
        action = combat_action_registry[action_id]
        action(
            self.state,
            self.owner,
            self.targets,
            self.spell_def
        )

    def do_finish(self):
        self.done = True

    def show_spell_notice(self):
        self.state.show_notice(self.spell_def["name"])

    def hide_spell_notice(self):
        self.state.hide_notice()

    def time_points(self, queue):
        speed = self.owner.stats.get("speed")
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        self.state.stack.push(self.storyboard)
        self.remove_dead_enemies_as_targets()

    def remove_dead_enemies_as_targets(self):
        for target in list(self.targets):
            hp = target.stats.get("hp_now")
            is_enemy = not self.state.is_party_member(target)
            if is_enemy and hp <= 0:
                self.targets.remove(target)

        if len(self.targets) == 0:
            selector = getattr(
                CombatSelector, self.spell_def["target"]["selector"])
            self.targets = selector(self.state)

    def is_finished(self):
        return self.done

    def update(self):
        pass
