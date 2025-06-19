from assets import palette
from script.textEngine.text import TextEditor


class CodeEditor(TextEditor):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(text, position, size, background, foreground, highlight_foreground,
                         font, font_size, margin, spacing)
        self.syntax = ""
        self.output = "hello wolrd!"

    def display_char(self, char, line, pointer, position):
        super().display_char(char, line, pointer, position)

    def display_text(self):
        #self.highlight_syntax()
        super().display_text()

    def highlight_syntax(self):
        self.syntax = ""
        string = None
        for i in self.text:
            if string is None:
                if i in ('"', "'"):
                    string = i
                    self.syntax += 's'
                else:
                    self.syntax += ' '
            else:
                if i == string:
                    string = None
                self.syntax += 's'

    def run(self):
        exec(self.text)