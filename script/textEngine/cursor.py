import pygame as p
from assets import palette


class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.blinkRate = 30
        self.blink = 0
        self.colour = palette.white

    def refresh(self, parent):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)
        location = parent.get_location(position = self.position)
        if self.blink < self.blinkRate:
            p.draw.rect(parent.surface, self.colour, (location[0], location[1], 1, parent.font.height))

