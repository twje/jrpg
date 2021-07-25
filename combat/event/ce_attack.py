from storyboard.storyboard import Storyboard
from storyboard import events


class CEAttack:
    # stack
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
                events.run_state(self.controller, "cs_run_anim", {"anim": "attack", "loop": False}),  # bug
                events.run_state(self.controller, "cs_move", {"dir": -1}),                
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
