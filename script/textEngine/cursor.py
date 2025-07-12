import pygame as p
import math
import settings
from assets import palette


def better_round(number):
    if number - int(number) < 0.5:
        return math.floor(number)
    return math.ceil(number)


class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.location = None
        self.targetLocation = [0, 0]
        self.moving = False
        self.blinkRate = settings.cursorBlinkRate
        self.blink = 0
        self.colour = palette.white
        self.surface = p.Surface((0, 0))

    def refresh(self, parent):
        if self.position is None:
            return
        self.targetLocation = [better_round(i) for i in parent.get_location(position = self.position)]
        self.targetLocation[1] += better_round(parent.font.height / 10)
        if self.location == self.targetLocation:
            self.moving = False

        if self.location is None or not settings.smoothCursor:
            self.location = self.targetLocation
            self.moving = True
        elif self.location != self.targetLocation:
            for i in range(2):
                if self.location[i] < self.targetLocation[i]:
                    self.location[i] = math.ceil((self.location[i] + self.targetLocation[i]) / 2)
                else:
                    self.location[i] = math.floor((self.location[i] + self.targetLocation[i]) / 2)
            self.moving = True

    def _display(self, parent):
        parent.display(self.surface, [self.location[i] - parent.offset[i] for i in range(2)])

    def display(self, parent):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)

        self.surface = p.transform.scale(self.surface, (1, parent.font.height * 4 / 5))
        self.surface.fill(self.colour)

        if settings.cursorAnimation:
            tick = self.blink / self.blinkRate
            alpha = (tick - int(tick)) if int(tick) % 2 else int(tick) - tick + 1
            self.surface.set_alpha(round(255 * max(0.0, min(1.0, 2 * alpha ** 2))))
            self._display(parent)
        elif self.blink < self.blinkRate:
            self._display(parent)




