from . import register_state


@register_state("ce_attack")
class CEAttack:
    def __init__(self, scene, owner, target):
        self.scene = scene
        self.owner = owner
        self.target = target
        self.name = f"CEAttack({owner.name}, {target.name})"

    def time_points(self, queue):
        speed = self.owner.speed
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        target = self.target
        if target.HP == 0:
            # new random target
            target = self.scene.get_target(self.owner)

        demage = self.owner.attack
        target.HP -= demage

        msg = "{} hit for {} demage".format(
            target.name,
            demage
        )
        print(msg)

        if target.HP < 0:
            msg = f"{self.target.name} is killed."
            print(msg)

            self.scene.on_dead(target)

    def update(self):
        pass

    def is_finished(self):
        return True
