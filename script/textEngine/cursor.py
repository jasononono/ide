import pygame as p
from assets import palette


class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.location = [0, 0]
        self.blinkRate = 30
        self.blink = 0
        self.colour = palette.white
        self.surface = p.Surface((1, 1))

    def refresh(self, parent):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)
        location = parent.get_location(position = self.position)
        if self.location is None:
            self.location = location
        else:
            self.location = [round((i + j) / 2) for i, j in zip(self.location,
                                                                (location[0], location[1] + parent.font.height / 10))]

        tick = self.blink / self.blinkRate
        alpha = (tick - int(tick)) if int(tick) % 2 else int(tick) - tick + 1
        alpha = min(255.0, 2 * alpha ** 2)

        self.surface = p.transform.scale(self.surface, (1, parent.font.height * 4 / 5))
        self.surface.set_alpha(round(255 * alpha))
        self.surface.fill(self.colour)
        parent.display(self.surface, self.location)
