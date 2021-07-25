class CEAttack:
    # stack
    def __init__(self, state, owner, attack_def, targets):
        self.state = state
        self.owner = owner
        self.targets = targets
        self.character = state
        self.name = f"Attack for {self.owner.name}"
        self.done = False
        self.controller = self.character.contoller

    def time_points(self, queue):
        speed = self.owner.stats.get('speed')
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        pass

    def update(self):
        pass

    def is_finished(self):
        return self.done
