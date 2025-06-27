import io, sys, traceback

from assets import palette
from script.textEngine.action import EditAction
from script.textEngine.text import FancyDisplay, TextEditor


class CodeEditor(TextEditor):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0),
                 output_channel = None):
        super().__init__(text, position, size, background, foreground, highlight_foreground,
                         font, font_size, margin, spacing)
        from script.textEngine.keymap import code_keymap
        self.action = EditAction(code_keymap)

        self.keywords = ("False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue",
                         "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import",
                         "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while",
                         "with", "yield", "match", "case")
        self.builtins = ("abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray",
                         "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir",
                         "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr",
                         "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
                         "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct",
                         "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "self", "set",
                         "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars",
                         "zip")

        self.outputChannel = output_channel

    def display_text(self, event):
        self.highlight_syntax()
        super().display_text(event)

    def highlight_token(self, index, token, next_token = None):
        if not token or token.isspace():
            return None
        for i in range(len(token)):
            if next_token in ("def", "class"):
                self.textEffects[index + i].colour = palette.blue
            if token in self.keywords:
                self.textEffects[index + i].colour = palette.orange
            elif token in self.builtins:
                self.textEffects[index + i].colour = palette.purple
        if token == "def":
            return "def"
        if token == "class":
            return "class"
        return None

    def highlight_syntax(self):
        token = ""
        token_start = 0
        next_token = None
        i = 0
        while i < len(self.text):
            self.textEffects[i].colour = None
            if self.text[i].lower() in "qwertyuiopasdfghjklzxcvbnm1234567890_":
                if not token:
                    token_start = i
                token += self.text[i]
            else:
                next_token = self.highlight_token(token_start, token, next_token)
                token = ""
                if self.text[i].lower() == '.':
                    token += '.'
                elif self.text[i] in "'\"":
                    string = self.text[i]
                    self.textEffects[i].colour = palette.green
                    i += 1
                    while i < len(self.text):
                        self.textEffects[i].colour = palette.green
                        if self.text[i] == string:
                            break
                        i += 1
                elif self.text[i] == '#':
                    self.textEffects[i].colour = palette.grey
                    i += 1
                    while i < len(self.text):
                        self.textEffects[i].colour = palette.grey
                        if self.text[i] == '\n':
                            break
                        i += 1
            i += 1
        self.highlight_token(token_start, token, next_token)

    def print(self, text, colour = None):
        if isinstance(self.outputChannel, FancyDisplay):
            self.outputChannel.append(text, colour)
        elif self.outputChannel:
            self.outputChannel.append(text)

    def run(self):
        self.outputChannel.erase()
        output = io.StringIO()
        error = io.StringIO()
        stdout, sys.stdout = sys.stdout, output
        stderr, sys.stderr = sys.stderr, error

        try:
            exec(self.text)
            self.print(output.getvalue() + "\nprocess finished with exit code 0")
        except Exception as e:
            exception = traceback.extract_tb(e.__traceback__)[1:]
            error.write("Traceback (most recent call last):\n" + "".join(traceback.format_list(exception)) +
                        f"{type(e).__name__}: {e}\n")
            self.print(error.getvalue(), palette.red)
            self.print("\nprocess finished with exit code 1")

        sys.stdout = stdout
        sys.stderr = stderr