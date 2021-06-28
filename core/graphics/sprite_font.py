from .sprite import BaseSprite
from .texture import Texture
import pygame
import utils


# ------------
# Font Loaders
# ------------
class SystemFont:
    def __init__(self, name):
        self.name = name

    def load(self, size):
        return pygame.font.SysFont(self.name, size)


class TTFFont:
    def __init__(self, filename=None):
        self.filename = filename

        # default
        if self.filename is None:
            self.filename = pygame.font.get_default_font()

    def load(self, size):
        return pygame.font.Font(self.filename, size)


# ----------
# Font Style
# ----------
class FontStyle:
    def __init__(self, font_loader, size, antialias=False, bold=False,
                 italic=False, underline=False, color=(255, 255, 255, 255)):
        self.font_loader = font_loader
        self.size = size
        self.antialias = antialias
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.color = color

    @property
    def font(self):
        font = self.font_loader.load(self.size)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        font.set_underline(self.underline)

        return font

    @classmethod
    def small(cls):
        return cls(
            font_loader=TTFFont(),
            size=15,
            antialias=True,            
        )

    @classmethod
    def default(cls):
        return cls(
            font_loader=TTFFont(),
            size=20,
            antialias=True
        )

    @classmethod
    def textbox_title(cls):
        return cls(
            font_loader=TTFFont(),
            size=16,
            bold=True,
            color=(251, 179, 92, 255),
            antialias=True
        )

    @classmethod
    def npc_dialogue(cls):
        return cls(
            font_loader=TTFFont(),
            size=16,
            bold=False,
            color=(255, 255, 255, 255),
            antialias=True
        )

    @classmethod
    def storyboard_title(cls):
        return cls(
            font_loader=TTFFont(utils.lookup_font_filepath("title")),
            size=30,
            bold=True,
            color=(255, 255, 255, 255),
            antialias=True
        )


# ----
# Font
# ----
class Font:
    def __init__(self, style=FontStyle.default()):
        self.style = style
        self.font = self.style.font

    def apply_style(self, style):
        self.font = self.loader.load(style.size)
        self.font.set_bold(style.bold)
        self.font.set_italic(style.italic)
        self.font.set_underline(style.underline)

        self.style = style

    def render(self, text, antialias, color, background=None):
        return self.font.render(text, antialias, color, background)

    def height(self):
        return self.font.size("Tg")[1]

    def width(self, text):
        return self.font.size(text)[0]


# ----------
# SpriteFont
# ----------
class SpriteFont(BaseSprite):
    def __init__(self, text=None, font=None):
        super().__init__()
        self.font = Font() if font is None else font
        self.text = None
        self.texture = None
        self.set_text(text)

    def set_font_style(self, style):
        self.font.apply_style(style)
        self.set_text(self.text)

    def set_text(self, text):
        if text is None:
            return

        self.text = self.format_text(text)
        self.rasterize()

    def set_alpha(self, alpha):
        self.rasterize(alpha)

    def rasterize(self, alpha=1):
        style = self.font.style
        surface = pygame.Surface(self.rasterize_bounds(), pygame.SRCALPHA)
        for index, row in enumerate(self.text):
            text_surface = self.font.render(
                row,
                style.antialias,
                style.color
            )
            y = index * self.font.height()
            surface.blit(text_surface, (0, y))
            surface.set_alpha(int(alpha * 255))
        self.texture = Texture(surface)

    def rasterize_bounds(self):
        width = max([self.font.width(row) for row in self.text])
        height = self.font.height() * len(self.text)

        return (width, height)

    # Sprite Font
    def validate(self):
        return self.texture is not None

    @staticmethod
    def format_text(text):
        # split
        try:
            return text.strip().split("\n")
        # already split
        except AttributeError:
            return [row.strip() for row in text]
