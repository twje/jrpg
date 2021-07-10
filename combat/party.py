"""
The party class records the characters in the party.
"""


class Party:
    def __init__(self):
        self.members = {}

    def add(self, actor):
        self.members[actor.id] = actor

    def remove_by_id(self, actor_id):
        del self.members[actor_id]

    def remove(self, actor):
        del self.members[actor.id]

    def to_list(self):
        return list(self.members.values())