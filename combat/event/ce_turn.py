from combat.combat_choice_state import CombatStateChoice


class CETurn:
    # event queue
    def __init__(self, state, owner):
        self.state = state
        self.owner = owner
        self.name = f"Turn for {owner.name}"
        self.done = False

    def time_points(self, queue):
        speed = self.owner.stats.get("speed")  # fix - check speed stat
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        if self.state.is_party_member(self.owner):
            state = CombatStateChoice(self.state, self.owner)
            self.state.stack.push(state)
            self.done = True
            return
        else:
            self.done = True
            # query AI for task

    def update(self):
        pass

    def is_finished(self):
        return self.done
