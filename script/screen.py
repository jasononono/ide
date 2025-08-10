import pygame as p
from script.utility import Object, Event
from assets import palette

from script.textEngine.text import TextDisplay, StaticDisplay
from script.code import CodeEditor
from script.button import Button


class Screen(Object):
    def __init__(self, size = (1200, 600)):
        super().__init__((0, 0), size)
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.event = Event()
        self.execute = True

        self.output = TextDisplay("IDE", (800, 10), (390, 580), font_size = 13,
                                  margin = (10, 10), spacing = (0, 3))

        self.text = CodeEditor("", (210, 10), (580, 580), font_size = 13,
                               margin = (10, 10), spacing = (0, 3), output_channel = self.output)

        self.title = StaticDisplay("this is an ide lol\n\nctrl-r: run code\nctrl-v/c/x:\n   I believe the function of"
                                   "\n   these keys are kinda\n   obvious\n\nwrite you program in\npython plz",
                                 (10, 10), (190, 400), font_size = 13, font = "inter")

        self.testButton = Button((0, 0), (100, 202))

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False
        if self.event.detect(p.MOUSEMOTION):
            p.mouse.set_visible(True)

        self.surface.fill(palette.dark1)
        self.event.cursor = p.SYSTEM_CURSOR_ARROW

        self.text.refresh(self, self.event)
        self.output.refresh(self, self.event)
        self.title.refresh(self, self.event)

        # if self.testButton.refresh(self, self.event):
        #     print("esr")
