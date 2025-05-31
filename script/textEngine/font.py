import pygame as p
import string
from assets import palette


class Font:
    def __init__(self, size, name = None, bold = False, italic = False,
                 foreground = palette.white, background = None):
        self.size = size
        self.name = "jetBrainsMono" if name is None else name
        self.modifier = ("bolditalic" if italic else "bold") if bold else ("italic" if italic else "regular")
        self.foreground = foreground
        self.background = background

        self.template = p.font.Font(f"assets/typeface/{self.name}/{self.name}-{self.modifier}.ttf", size)
        self.glyphs = {i: j[4] for i, j in zip(string.printable, self.template.metrics(string.printable))}
        self.height = self.template.get_height()

    def render(self, text, foreground = None, background = None):
        return self.template.render(text, True, self.foreground if foreground is None else foreground,
                                    self.background if background is None else background)