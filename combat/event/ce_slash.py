from anim_entity_fx import AnimEntityFx
from combat import combat_formula
from core import Context
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.combat_target_state import CombatSelector


class CESlash:
    def __init__(self, state, owner, special_def, targets):
        context = Context.instance()
        self.entity_defs = context.data["entity_definitions"]
        self.state = state
        self.owner = owner
        self.special_def = special_def
        self.targets = targets
        self.name = f"Slash for {owner.name}"
        self.character = state.actor_char_map[owner]
        self.entity = self.character.entity
        self.controller = self.character.controller
        self.done = False

        self.storyboard = Storyboard(
            self.state.stack, [
                events.function(self.show_notice),
                events.wait(0.2),
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.run_state(self.controller, "cs_run_anim", {
                    "anim": "slash", "loop": False, "spf": 0.05}),
                events.no_block(
                    events.run_state(self.controller, "cs_run_anim", {
                                     "anim": "prone"}),
                ),
                events.function(self.do_attack),
                events.run_state(self.controller, "cs_move", {"dir": -1}),
                events.wait(0.2),
                events.function(self.on_finish)
            ])

    def do_attack(self):
        self.state.hide_notice()
        mp = self.owner.stats.get("mp_now")
        cost = self.special_def["mp_cost"]
        mp = max(mp - cost, 0)
        self.owner.stats.set("mp_now", mp)

        for target in self.targets:
            self.attack_target(target)

            if self.special_def.get("counter", False):
                self.counter_target(target)

    def attack_target(self, target):
        demage, hit_result = combat_formula.malee_attack(
            self.state,
            self.owner,
            target
        )

        if hit_result == combat_formula.HitResult.MISS:
            self.state.apply_miss(target)
            return
        elif hit_result == combat_formula.HitResult.DODGE:
            self.state.apply_dodge(target)
        else:
            is_crit = hit_result == combat_formula.HitResult.CRITICAL
            self.state.apply_demage(target, demage, is_crit)

        entity_def = self.entity_defs.get_entity_def("slash")
        target_entity = self.state.actor_char_map[target].entity
        target_position = target_entity.sprite.get_position()
        effect = AnimEntityFx(
            target_position[0],
            target_position[1],
            entity_def,
            entity_def["frames"],
        )
        self.state.add_effect(effect)

    def counter_target(self, target):
        is_countered = combat_formula.is_countered(
            self.state, self.owner, target)
        if is_countered:
            self.state.apply_counter(target, self.owner)

    def show_notice(self):
        self.state.show_notice(self.special_def["name"])

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

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
            self.targets = CombatSelector.side_enemy(self.state)

    def is_finished(self):
        return self.done
