import pygame as p


class Event:
    def __init__(self):
        self.event = None
        self.key = None
        self.mouse = None
        self.mousePosition = None
        self.refresh()

    def refresh(self):
        self.event = p.event.get()
        self.key = p.key.get_pressed()
        self.mouse = p.mouse.get_pressed()
        self.mousePosition = p.mouse.get_pos()

    def detect(self, event):
        for e in self.event:
            if e.type == event:
                return True
        return False

    def key_down(self, key):
        return self.detect(p.KEYDOWN) and self.key[key]

    def mouse_down(self):
        return self.detect(p.MOUSEBUTTONDOWN)

    def mouse_up(self):
        return self.detect(p.MOUSEBUTTONUP)


class Rect(p.Rect):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.abs = self.copy()

    def refresh(self, rect):
        self.abs.topleft = (self.x + rect.abs.x, self.y + rect.abs.y)
        self.abs.size = self.size


class Object:
    def __init__(self, position, size):
        self.surface = p.Surface(size)
        self.rect = Rect(position, size)

    def display(self, surface, position = (0, 0)):
        self.surface.blit(surface, position)