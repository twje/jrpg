class CEUseItem:
    def __init__(self, state, owner, item, targets):
        pass

    def time_points(self, queue):
        speed = self.owner.stats.get("speed")
        return queue.speed_to_time_points(speed)
    
    def show_item_notice(self):
        pass

    def do_use_item(self):
        pass

    def do_finish(self):
        pass

    def execute(self):
        pass

    def is_finished(self):
        pass

    def update(self, dt):
        pass