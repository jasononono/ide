import pygame as p
import settings
from assets import palette


class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.location = None
        self.blinkRate = 30
        self.blink = 0
        self.colour = palette.white
        self.surface = p.Surface((1, 1))

    def refresh(self, parent):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)
        location = parent.get_location(position = self.position)
        if self.location is None or not settings.cursorAnimation:
            self.location = location
        else:
            self.location = [round((i + j) / 2) for i, j in zip(self.location,
                                                                (location[0], location[1] + parent.font.height / 10))]

        self.surface = p.transform.scale(self.surface, (1, parent.font.height * 4 / 5))
        self.surface.fill(self.colour)

        if settings.smoothCursor:
            tick = self.blink / self.blinkRate
            alpha = (tick - int(tick)) if int(tick) % 2 else int(tick) - tick + 1
            self.surface.set_alpha(round(255 * min(255.0, 2 * alpha ** 2)))
            parent.display(self.surface, self.location)
        elif self.blink < self.blinkRate:
            parent.display(self.surface, self.location)





