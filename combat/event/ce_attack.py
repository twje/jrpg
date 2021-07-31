from combat.combat_target_state import CombatSelector
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.fx import AnimEntityFX
from core import Context
from combat import combat_formula

class CEAttack:
    # event queue - orchestrate stack using storyboard
    def __init__(self, state, owner, attack_def, targets):
        self.state = state
        self.owner = owner
        self.targets = targets
        self.character = state.actor_char_map[owner]
        self.name = f"Attack for {self.owner.name}"
        self.done = False
        self.controller = self.character.controller
        self.context = Context.instance()

        # prime combat event
        self.controller.change("cs_run_anim", {"anim": "prone"})
        self.storyboard = Storyboard(
            self.state.stack, [
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.run_state(self.controller, "cs_run_anim", {
                                 "anim": "attack", "loop": False}),
                events.function(self.do_attack),
                events.run_state(self.controller, "cs_move", {"dir": -1}),
                events.function(self.on_finish),
            ])

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        self.state.stack.push(self.storyboard)

        # prevent attacking a dead target
        for target in list(self.targets):
            hp = target.stats.get("hp_now")
            if hp <= 0:
                self.targets.remove(target)

        if len(self.targets) == 0:
            self.targets = CombatSelector.weakest_enemy(self.state)

    def update(self):
        pass

    def is_finished(self):
        return self.done

    def do_attack(self):
        for target in self.targets:
            self.attack_target(target)

    def attack_target(self, target):
        demage = combat_formula.malee_attack(self.state, self.owner, target)
        self.state.apply_demage(target, demage)
        self.add_slash_effects(target, demage)


    def add_slash_effects(self, target, demage):        
        character = self.state.actor_char_map[target]
        entity = character.entity
        entity_defs = self.context.data["entity_definitions"]
        entity_def = entity_defs.get_entity_def("slash")
        slash_effect = AnimEntityFX(
            entity.sprite.x + entity.width/2,
            entity.sprite.y + entity.height/2,
            entity_def,
            entity_def["frames"]
        )
        self.state.add_effect(slash_effect)

    def on_finish(self):
        self.done = True
