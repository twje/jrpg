class ProgressBar:
    def __init__(self, parms):
        self.x = parms.get("x", 0)
        self.y = parms.get("y", 0)
        self.foreground = parms["foreground"]
        self.background = parms["background"]
        self.value = parms.get("value", 0)
        self.maximum = parms.get("maximum", 1)

        self.set_value(self.value)
        self.set_position(self.x, self.y)

    # ---
    # API
    # ---
    def scale(self, value):
        self.foreground.scale_by_ratio(value, 1)
        self.background.scale_by_ratio(value, 1)

    def set_value(self, value, maximum=None):
        if maximum:
            self.maximum = maximum
        self.set_normal_value(value/self.maximum)

    def set_position(self, x, y):
        self.background.set_position(x, y)
        self.foreground.set_position(x, y)

    def get_position(self, x, y):
        return x, y

    def render(self, renderer):
        renderer.draw(self.background)
        renderer.draw(self.foreground)

    # --------------
    # Helper Mothods
    # --------------
    def set_normal_value(self, value):
        self.foreground.scale_by_ratio(value, 1)
