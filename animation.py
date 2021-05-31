class Animation:
    def __init__(self, frames, loop=True, spf=0.12):
        self.frames = frames
        self.loop = loop
        self.spf = spf
        self.index = 0
        self.time = 0

    def update(self, dt):
        self.time += dt

        if self.time >= self.spf:
            self.index += 1
            self.time = 0

            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames)

    def set_frames(self, frames):
        self.frames = frames
        self.index = min(self.index, len(frames) - 1)

    def frame(self):
        return self.frames[self.index]

    def is_finished(self):
        return self.loop and self.index == len(self.frames)
