
from combat.event_queue import EventQueue
from state_machine.combat.event.ce_turn import CETurn


class CombatScene:
    def __init__(self, party, enemies):
        self.party_actors = party
        self.enemy_actors = enemies
        self.event_queue = EventQueue()

    def add_turns(self, actor_list):
        for actor in actor_list:
            if not self.event_queue.actor_has_event(actor):
                event = CETurn(self, actor)
                tp = event.time_points(self.event_queue)
                self.event_queue.add(event, tp)

    def update(self):
        self.event_queue.update()

        if self.is_party_defeated() or self.is_enemy_defeated():
            # end game
            self.event_queue.queue.clear()
        else:
            self.add_turns(self.party_actors)
            self.add_turns(self.enemy_actors)

    def on_dead(self, actor):
        if actor.is_player():
            actor.ko()
        else:
            for enemy in list(self.enemy_actors):
                if enemy == actor:
                    self.enemy_actors.remove(actor)

        self.event_queue.removed_events_owned_by(actor)

        if self.is_party_defeated():
            print("Party loses")
        elif self.is_enemy_defeated():
            print("Party wins")

    def get_target(self, actor):
        target_list = None

        if actor.is_player():
            target_list = self.enemy_actors
        else:
            target_list = self.get_live_party_actors()

        return target_list[-1]  # random

    def get_live_party_actors(self):
        live = []
        for actor in self.party_actors:
            if not actor.is_koed():
                live.append(actor)
        return live

    def is_party_defeated(self):
        for actor in self.party_actors:
            if not actor.is_koed():
                return False
        return True

    def is_enemy_defeated(self):
        return len(self.enemy_actors) == 0
