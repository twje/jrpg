from combat.combat_choice_state import CombatStateChoice


class CEAttack:
    def __init__(self):
        pass

    def time_points(self, queue):
        speed = self.owner.speed
        return queue.speed_to_time_points(speed)

    def execute(self, queue):
        pass
        # target = self.target
        # if target.HP == 0:
        #     # new random target
        #     target = self.scene.get_target(self.owner)

        # demage = self.owner.attack
        # target.HP -= demage

        # msg = "{} hit for {} demage".format(
        #     target.name,
        #     demage
        # )
        # print(msg)

        # if target.HP < 0:
        #     msg = f"{self.target.name} is killed."
        #     print(msg)

        #     self.scene.on_dead(target)

    def update(self):
        pass

    def is_finished(self):
        return True
