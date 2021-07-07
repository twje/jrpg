from collections import deque
import math


class Event:
    def __init__(self, name):
        self.name = name
        self.count_down = -1
        self.owner = None

    def execute():
        pass

    def update():
        pass

    def is_finished():
        pass

    def __repr__(self):
        return "Event({!r}, {!r})".format(self.name, self.count_down)


class EventQueue:
    def __init__(self):
        self.queue = deque()
        self.current_event = None

    def add(self, event, time_points):
        if time_points == -1:
            event.count_down = -1
            self.queue.appendleft(event)
        else:
            event.count_down = time_points
            for index, item in enumerate(self.queue):
                count = item.count_down
                if count > event.count_down:
                    self.queue.insert(index, event)
                    return
            self.queue.append(event)

    def speed_to_time_points(self, speed):
        max_speed = 255
        speed = min(speed, 255)
        points = max_speed - speed
        return math.floor(points)

    def update(self):
        if self.current_event != None:
            self.update_event()
        elif not self.is_empty():
            self.choose_event()
            self.decrement_count_down()

    def update_event(self):
        self.current_event.update()
        if self.current_event.is_finished():
            self.current_event = None

    def choose_event(self):
        front = self.queue.popleft()
        front.execute(self)
        self.current_event = front

    def decrement_count_down(self):
        for event in self.queue:
            event.count_down = max(0, event.count_down - 1)

    def clear(self):
        self.queue = deque()
        self.current_event = None

    def is_empty(self):
        return len(self.queue) == 0

    def actor_has_event(self, actor):
        current = Event("") if self.current_event is None else self.current_event
        if current.owner == actor:
            return True

        for event in self.queue:
            if event.owner == actor:
                return True

        return False

    def removed_events_owned_by(self, actor):
        for event in list(self.queue):
            if event.owner == actor:
                self.queue.remove(event)

    def __repr__(self):
        return repr(self.queue)


# test = EventQueue()
# test.add(Event("Msg: Welcome to the Arena"), -1)
# test.add(Event("Take Turn Goblin"), 5)
# test.add(Event("Take Turn Hero"), 4)

# print(test)
