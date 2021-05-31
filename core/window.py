import pygame


class Window:
    def __init__(self, size, caption):
        self.size = size
        self.caption = caption
        self.bits = 32
        self.window_surface = None
        self.is_done = False
        self.is_fullscreen = False
        self.event_callback = None
        self.create()

    def create(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.window_surface = pygame.display.set_mode(self.size, 0, self.bits)

    def destroy(self):
        pygame.quit()

    def toggle_full_screen(self):
        # capture state
        flags = self.window_surface.get_flags()
        tmp = self.window_surface.convert()

        # toggle
        self.window_surface = pygame.display.set_mode(
            self.size, flags ^ pygame.FULLSCREEN, self.bits)

        # restore state
        self.window_surface.blit(tmp, (0, 0))
        pygame.display.set_caption(self.caption)
        pygame.key.set_mods(0)

        self.is_fullscreen = not self.is_fullscreen

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.toggle_full_screen()

            if self.event_callback:
                self.event_callback(event)

    def begin_draw(self):
        self.window_surface.fill((0, 0, 0))

    def draw(self):
        pass

    def end_draw(self):
        pygame.display.flip()
