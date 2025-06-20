import io, sys, traceback

from assets import palette
from script.textEngine.action import EditAction
from script.textEngine.text import TextEditor


class CodeEditor(TextEditor):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(text, position, size, background, foreground, highlight_foreground,
                         font, font_size, margin, spacing)
        from script.textEngine.keymap import code_keymap
        self.action = EditAction(code_keymap)

        self.syntax = ""
        self.output = ""

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
        self.output = "/Users/dummy/Documents/untitled.py\n"
        output = io.StringIO()
        error = io.StringIO()
        stdout, sys.stdout = sys.stdout, output
        stderr, sys.stderr = sys.stderr, error

        try:
            exec(self.text)
            self.output += output.getvalue() + "\nprocess finished with exit code 0"
        except Exception as e:
            exception = traceback.extract_tb(e.__traceback__)[1:]
            # exception = [i._replace()
            #              for i in traceback.extract_tb(e.__traceback__)[1:]]
            error.write("Traceback (most recent call last):\n" + ''.join(traceback.format_list(exception)) +
                        f"{type(e).__name__}: {e}\n")
            self.output += error.getvalue() + "\nprocess finished with exit code 1"

        sys.stdout = stdout
        sys.stderr = stderr