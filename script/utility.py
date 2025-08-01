import pygame as p


class Event:
    def __init__(self):
        self.event = None
        self.key = None
        self.mouse = None
        self.mousePosition = None
        self.active = None
        self.cursor = p.SYSTEM_CURSOR_ARROW
        self.refresh()

    def refresh(self):
        self.event = p.event.get()
        self.key = p.key.get_pressed()
        self.mouse = p.mouse.get_pressed()
        self.mousePosition = p.mouse.get_pos()
        p.mouse.set_cursor(self.cursor)

    def detect(self, event):
        for e in self.event:
            if e.type == event:
                return e
        return None

    def detect_all(self, event):
        return [e for e in self.event if e.type == event]

    def key_down(self, key = None):
        event = self.detect_all(p.KEYDOWN)
        keys = [i.key for i in event]
        if key is None:
            if event:
                return keys
            return []
        return key in keys if event else None

    def key_up(self, key = None):
        event = self.detect_all(p.KEYUP)
        keys = [i.key for i in event]
        if key is None:
            if event:
                return keys
            return []
        return key in keys if event else None

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
    def __init__(self, position = (0, 0), size = (0, 0), alpha = False):
        self.surface = p.Surface(size, p.SRCALPHA) if alpha else p.Surface(size)
        self.rect = Rect(position, size)

    def resize(self, size = (0, 0)):
        self.surface = p.transform.scale(self.surface, size)
        self.rect.size = size

    def display(self, surface, position = (0, 0)):
        self.surface.blit(surface, position)

    def fill(self, *args, **kwargs):
        self.surface.fill(*args, **kwargs)

    def draw_rect(self, *args, **kwargs):
        p.draw.rect(self.surface, *args, **kwargs)

    def draw_line(self, *args, **kwargs):
        p.draw.line(self.surface, *args, **kwargs)

    def valid_mouse_position(self, position):
        return self.rect.abs.collidepoint(position)

