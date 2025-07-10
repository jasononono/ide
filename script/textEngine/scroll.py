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
        if not parent.realSize or parent.rect.size[self.side] >= parent.realSize[self.side]:
            return False

        length = parent.rect.size[self.side] ** 2 / parent.realSize[self.side]
        size = (self.width, length) if self.side else (length, self.width)

        position = (self.position[self.side] + parent.offset[self.side] /
                    (parent.realSize[self.side] - parent.rect.size[self.side]) *
                    (parent.rect.size[self.side] - size[self.side]))
        self.rect.topleft = (self.position[0], position) if self.side else (position, self.position[1])

        self.resize(size)
        self.fill(palette.white)
        self.rect.refresh(parent.rect)

        if self.pressed:
            event.cursor = p.SYSTEM_CURSOR_ARROW
            self.surface.set_alpha(200)
            percent = ((event.mousePosition[self.side] - parent.rect.abs.topleft[self.side] - self.location) /
                       (parent.rect.size[self.side] - size[self.side]))
            parent.offset[self.side] = (max(0, min(1, percent)) *
                                        (parent.realSize[self.side] - parent.rect.size[self.side]))
        elif self.valid_mouse_position(event.mousePosition):
            event.cursor = p.SYSTEM_CURSOR_ARROW
            self.surface.set_alpha(150)
            if event.mouse_down():
                self.pressed = True
                self.location = event.mousePosition[self.side] - self.rect.abs.topleft[self.side]
        else:
            self.surface.set_alpha(100)
        if event.mouse_up():
            self.pressed = False

        parent.display(self.surface, self.rect)
        return self.pressed