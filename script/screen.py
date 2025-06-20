import pygame as p
from script.utility import Object, Event
from assets import palette

from script.textEngine.text import TextDisplay
from script.textEngine.code import CodeEditor


class Screen(Object):
    def __init__(self, size = (1000, 600)):
        super().__init__((0, 0), size)
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.event = Event()
        self.execute = True

        self.output = TextDisplay("Beta IDE", (600, 10), (390, 580), font_size = 13,
                                  margin = (10, 10), spacing = (0, 3))

        self.text = CodeEditor("", (10, 10), (580, 580), font_size = 13,
                               margin = (10, 10), spacing = (0, 3), output_channel = self.output)

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False
        if self.event.detect(p.MOUSEMOTION):
            p.mouse.set_visible(True)

        self.surface.fill(palette.dark1)
        p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)

        self.text.refresh(self, self.event)
        self.output.refresh(self, self.event)
