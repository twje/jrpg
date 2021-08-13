import random


class OddmeantTable:
    def __init__(self, items):
        self.items = items

    @property
    def oddment(self):
        return sum(item["oddment"] for item in self.items)

    def pick(self):
        select = random.randint(0, self.oddment)

        total = 0
        for item in self.items:
            total += item["oddment"]

            if total >= select:
                return item["item"]
