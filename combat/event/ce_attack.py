from combat.combat_target_state import CombatSelector
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.fx import JumpingNumbers
from combat.fx import AnimEntityFX
from core import Context

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
        stats = self.owner.stats
        enemy_stats = target.stats

        # simple attack
        attack = stats.get("attack")
        attack += stats.get("strength")
        defense = enemy_stats.get("defence")

        demage = max(0, attack - defense)
        hp = enemy_stats.get("hp_now")
        hp = hp - demage

        enemy_stats.set("hp_now", max(0, hp))

        if demage > 0:
            self.set_hurt_state(target)

        self.add_effects(target, demage)

        # death is handled seperately so it occurs parallel with attack event
        self.state.handle_death()

    def add_effects(self, target, demage):
        character = self.state.actor_char_map[target]
        entity = character.entity

        # jumping number
        dmg_effect = JumpingNumbers(
            entity.sprite.x + entity.width/2,
            entity.sprite.y + entity.height/2,
            str(demage)
        )
        self.state.add_effect(dmg_effect)

        # slash
        entity_defs = self.context.data["entity_definitions"]
        entity_def = entity_defs.get_entity_def("slash")
        slash_effect = AnimEntityFX(
            entity.sprite.x + entity.width/2,
            entity.sprite.y + entity.height/2,
            entity_def,
            entity_def["frames"]
        )
        self.state.add_effect(slash_effect)

    def set_hurt_state(self, target):
        character = self.state.actor_char_map[target]
        controller = character.controller
        state = controller.current
        if state.name != "cs_hurt":
            controller.change("cs_hurt", {"state": state})

    def on_finish(self):
        self.done = True
