from combat.combat_formula import can_flee
from storyboard.storyboard import Storyboard
from storyboard import events


class CEFlee:
    def __init__(self, state, actor):
        self.state = state
        self.owner = actor
        self.character = state.actor_char_map[actor]
        self.flee_params = {"dir": 1, "distance": 180, "time": 0.6}
        self.done = False

        if can_flee(state, actor):
            self.storyboard = Storyboard(
                self.state.stack, [
                    events.function(lambda: self.notice(
                        "Attempting to Flee...")),
                    events.wait(0.75),
                    events.function(self.do_flee_success_part1),
                    events.wait(0.3),
                    events.function(self.do_flee_success_part2),
                    events.wait(0.6)
                ])
        else:
            self.storyboard = Storyboard(
                self.state.stack, [
                    events.function(lambda: self.notice(
                        "Attempting to Flee...")),
                    events.wait(0.75),
                    events.function(lambda: self.notice("Failed!")),
                    events.wait(0.3),
                    events.function(self.on_flee_fail)
                ])

        self.character.facing = "right"
        self.controller = self.character.controller
        self.controller.change("cs_run_anim", {"anim": "prone"})
        self.name = f"Flee for {self.owner.name}"

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

    def notice(self, text):
        self.state.show_notice(text)

    def do_flee_success_part1(self):
        self.notice("Success!")
        self.controller.change("cs_move", self.flee_params)

    def do_flee_success_part2(self):
        for actor in self.state.actors["party"]:
            alive = actor.stats.get("hp_now") > 0
            is_fleer = actor == self.owner

            if alive and not is_fleer:
                character = self.state.actor_char_map[actor]
                character.facing = "right"
                character.controller.change("cs_move", self.flee_params)

        self.state.on_flee()
        self.state.hide_notice()

    def on_flee_fail(self):
        self.character.facing = "left"
        controller = self.character.controller
        controller.change("cs_standby")
        self.done = True
        self.state.hide_notice()

    def execute(self, queue):
        self.state.stack.push(self.storyboard)

    def update(self):
        pass

    def is_finished(self):
        return self.done
