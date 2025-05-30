import pygame as p
from utility import Object, Event
from assets import palette

from textEngine.text import TextEditor


class Screen(Object):
    def __init__(self, size = (800, 600)):
        super().__init__((0, 0), size)
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.event = Event()
        self.execute = True

        self.text = TextEditor("class Screen(Object):\n    def __init__(self, size = (800, 600)):",
                                (10, 10), (780, 580), margin = (10, 10))

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False

        self.surface.fill(palette.dark1)
        p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)

        self.text.refresh(self, self.event)

        p.display.flip()