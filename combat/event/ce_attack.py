from combat.combat_target_state import CombatSelector
from storyboard.storyboard import Storyboard
from storyboard import events
from combat.fx import AnimEntityFX
from core import Context
from combat import combat_formula
from core.system.communication import SystemEvent


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
        self.event_dispatcher = self.context.event_dispatcher

        # prime combat event
        self.controller.change("cs_run_anim", {"anim": "prone"})

        if attack_def["player"]:
            self.attack_anim = self.get_entity_def("slash")
            self.default_targeter = CombatSelector.weakest_enemy

            self.storyboard = Storyboard(
                self.state.stack, [
                    events.run_state(self.controller, "cs_move", {"dir": 1}),
                    events.run_state(self.controller, "cs_run_anim", {
                                     "anim": "attack", "loop": False}),
                    events.function(self.do_attack),
                    events.run_state(self.controller, "cs_move", {"dir": -1}),
                    events.function(self.on_finish),
                ])
        else:
            self.attack_anim = self.get_entity_def("claw")
            self.default_targeter = CombatSelector.random_alive_player

            self.storyboard = Storyboard(
                self.state.stack, [
                    events.run_state(self.controller, "cs_move", {
                                     "dir": -1, "distance": 8, "time": 0.1}),
                    events.function(self.do_attack),
                    events.run_state(self.controller, "cs_move", {
                                     "dir": 1, "distance": 8, "time": 0.4}),
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
            self.targets = self.default_targeter(self.state)

    def update(self):
        pass

    def is_finished(self):
        return self.done

    def do_attack(self):
        for target in self.targets:
            self.attack_target(target)

    def attack_target(self, target):                
        demage = combat_formula.malee_attack(self.state, self.owner, target)
        entity = self.state.actor_to_entity(target)
        self.state.apply_demage(target, demage)
        self.add_attack_effect(entity)
        self.event_dispatcher.notify(SystemEvent.PLAY_SOUND, {"audio_id": "attack"})

    def add_attack_effect(self, entity):
        effect = AnimEntityFX(
            entity.sprite.x + entity.width/2,
            entity.sprite.y + entity.height/2,
            self.attack_anim,
            self.attack_anim["frames"]
        )
        self.state.add_effect(effect)

    def get_entity_def(self, entity_id):
        entity_defs = self.context.data["entity_definitions"]
        return entity_defs.get_entity_def(entity_id)

    def on_finish(self):
        self.done = True
