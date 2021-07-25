from storyboard.storyboard import Storyboard
from storyboard import events


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

        # prime combat event
        self.controller.change("cs_run_anim", {"anim": "prone"})
        self.storyboard = Storyboard(
            self.state.stack, [
                events.run_state(self.controller, "cs_move", {"dir": 1}),
                events.run_state(self.controller, "cs_run_anim", {"anim": "attack", "loop": False}),
                events.function(self.do_attack),
                events.run_state(self.controller, "cs_move", {"dir": -1}),                
                events.function(self.on_finish),
            ])

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        self.state.stack.push(self.storyboard)

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

        # death is handled seperately so it occurs parallel with attack event         
        self.state.handle_death()

    def on_finish(self):
        self.done  = True