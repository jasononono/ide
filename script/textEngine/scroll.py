import pygame as p

from script.utility import Object
from assets import palette

class Scroll(Object):
    def __init__(self, parent, position, side, width = 7):
        super().__init__(alpha = True)
        self.parent = parent
        self.side = side
        self.width = width
        self.position = position

        self.pressed = False
        self.location = 0

    def refresh(self, parent, event):
        if not parent.realSize:
            return False
        size = (parent.rect.size[0] ** 2 / parent.realSize[0], self.width)

        self.rect.top = self.position[1]
        self.rect.left = (self.position[0] + parent.offset[0] / (parent.realSize[0] - parent.rect.size[0]) *
                                             (parent.rect.size[0] - size[0]))
        self.resize(size)
        self.fill(palette.white)
        self.rect.refresh(parent.rect)

        if self.pressed:
            event.cursor = p.SYSTEM_CURSOR_ARROW
            self.surface.set_alpha(200)
            percent = (event.mousePosition[0] - parent.rect.abs.left - self.location) / (parent.rect.size[0] - size[0])
            parent.offset[0] = max(0, min(1, percent)) * (parent.realSize[0] - parent.rect.size[0])
        elif self.valid_mouse_position(event.mousePosition):
            event.cursor = p.SYSTEM_CURSOR_ARROW
            self.surface.set_alpha(150)
            if event.mouse_down():
                self.pressed = True
                self.location = event.mousePosition[0] - self.rect.abs.left
        else:
            self.surface.set_alpha(100)
        if event.mouse_up():
            self.pressed = False

        parent.display(self.surface, self.rect)
        return self.pressed