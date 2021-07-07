from combat.ce_attack import CEAttack


class CETurn:
    def __init__(self, scene, owner):
        self.scene = scene
        self.owner = owner
        self.name = f"CETurn({owner.name})"

    def time_points(self, queue):
        speed = self.owner.speed
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        target = self.scene.get_target(self.owner)
        msg = "{} decides to attack {}".format(
            self.owner.name,
            target.name
        )
        print(msg)
        event = CEAttack(self.scene, self.owner, target)
        tp = event.time_points(queue)
        queue.add(event, tp)

    def update(self):
        pass

    def is_finished(self):
        return True
