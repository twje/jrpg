import math


def linear(time_passed, start, distance, duration):
    return distance * time_passed / duration + start


def ease_out_quad(time_passed, start, distance, duration):
    time_passed = time_passed / duration
    return -distance * time_passed * (time_passed - 2) + start


def ease_in_circ(time_passed, start, distance, duration):
    time_passed = time_passed / duration
    return -distance * (math.sqrt(1 - time_passed * time_passed) - 1) + start


def ease_out_circ(time_passed, start, distance, duration):
    time_passed = time_passed / duration - 1
    return distance * math.sqrt(1 - time_passed * time_passed) + start


class Tween:
    def __init__(self, start, finish, total_duration, tween_callback=linear):
        self.start = start
        self.current = start
        self.finish = finish
        self.total_duration = total_duration
        self.tween_callback = tween_callback
        self.distance = finish - start
        self.time_passed = 0
        self.is_finished = False

    def finished_value(self):
        return self.start + self.distance

    def update(self, elapsed_time):
        self.time_passed += elapsed_time

        # cap by total_duration
        self.time_passed = min(self.time_passed, self.total_duration)

        self.current = self.tween_callback(
            self.time_passed,
            self.start,
            self.distance,
            self.total_duration
        )

        if self.time_passed >= self.total_duration:
            self.current = self.finished_value()
            self.is_finished = True

    @property
    def value(self):
        return self.current
