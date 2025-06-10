import pygame as p
from script.utility import Object, Event
from assets import palette

from script.textEngine.text import TextDisplay, TextEditor, CodeEditor


class Screen(Object):
    def __init__(self, size = (800, 600)):
        super().__init__((0, 0), size)
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.event = Event()
        self.execute = True

        self.text = TextEditor("", (10, 10), (780, 580), font_size = 15,
                               margin = (10, 10), spacing = (0, 3))

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False
        if self.event.detect(p.MOUSEMOTION):
            p.mouse.set_visible(True)

        self.surface.fill(palette.dark1)
        p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)

        self.text.refresh(self, self.event)
