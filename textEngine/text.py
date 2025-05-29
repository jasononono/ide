import pygame as p
from utility import Object
from assets import palette

from textEngine.font import Font


class TextDisplay(Object):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white,
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(position, size)
        self.text = text
        self.background = background
        self.foreground = foreground

        self.font = Font(font_size, font)
        self.margin = margin
        self.spacing = spacing

        self.map = []

    def refresh(self, parent, event):
        self.rect.refresh(parent.rect)

        self.surface.fill(self.background)
        self.display_text()
        parent.display(self.surface, self.rect)

    def display_char(self, char, line, pointer):
        if char != '\n':
            self.display(self.font.render(char),
                         (pointer, self.margin[1] + line * (self.font.height + self.spacing[1])))

    def display_text(self):
        self.map = [[]]
        pointer = self.margin[0]
        line = 0

        for i in self.text:
            self.display_char(i, line, pointer)
            if i == '\n':
                self.map.append([])
                pointer = self.margin[0]
                line += 1
            else:
                pointer += self.font.glyphs[i] + self.spacing[0]
                self.map[line].append(pointer)