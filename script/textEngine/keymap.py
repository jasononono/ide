import pygame as p

from script.textEngine.text import TextDisplay, TextEditor
from script.code import CodeEditor


class Key:
    def __init__(self, base = None, shift = None, ctrl = None, alt = None):
        self.base = base
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt


class Command:
    def __init__(self, function, repeat = True, follow = True):
        self.function = function
        self.repeat = repeat
        self.follow = follow

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class Keymap:
    def __init__(self):
        self.map = {}

    def assign(self, key, base = None, shift = None, ctrl = None, alt = None):
        self.map[key] = Key(base, shift, ctrl, alt)

    def retrieve(self, key, modifier = None):
        if modifier == "shift":
            return self.map[key].shift
        if modifier == "ctrl":
            return self.map[key].ctrl
        if modifier == "alt":
            return self.map[key].alt
        return self.map[key].base


view_keymap = Keymap()
view_keymap.assign(p.K_a, ctrl = TextDisplay.select_all)


edit_keymap = Keymap()

edit_keymap.assign(p.K_LEFT, Command(TextEditor.cursor_left), Command(TextEditor.highlight_left))
edit_keymap.assign(p.K_RIGHT, Command(TextEditor.cursor_right), Command(TextEditor.highlight_right))
edit_keymap.assign(p.K_DOWN, Command(TextEditor.cursor_down), Command(TextEditor.highlight_down))
edit_keymap.assign(p.K_UP, Command(TextEditor.cursor_up), Command(TextEditor.highlight_up))
edit_keymap.assign(p.K_BACKSPACE, Command(TextEditor.delete), Command(TextEditor.delete))
edit_keymap.assign(p.K_TAB, Command(TextEditor.indent))
edit_keymap.assign(p.K_RETURN, '\n')
edit_keymap.assign(p.K_SPACE, ' ', ' ')
edit_keymap.assign(p.K_1, '1', '!')
edit_keymap.assign(p.K_2, '2', '@')
edit_keymap.assign(p.K_3, '3', '#')
edit_keymap.assign(p.K_4, '4', '$')
edit_keymap.assign(p.K_5, '5', '%')
edit_keymap.assign(p.K_6, '6', '^')
edit_keymap.assign(p.K_7, '7', '&')
edit_keymap.assign(p.K_8, '8', '*')
edit_keymap.assign(p.K_9, '9', '(')
edit_keymap.assign(p.K_0, '0', ')')
edit_keymap.assign(p.K_BACKQUOTE, '`', '~')
edit_keymap.assign(p.K_MINUS, '-', '_')
edit_keymap.assign(p.K_EQUALS, '=', '+')
edit_keymap.assign(p.K_LEFTBRACKET, '[', '{')
edit_keymap.assign(p.K_RIGHTBRACKET, ']', '}')
edit_keymap.assign(p.K_BACKSLASH, '\\', '|')
edit_keymap.assign(p.K_SEMICOLON, ';', ':')
edit_keymap.assign(p.K_QUOTE, "'", '"')
edit_keymap.assign(p.K_COMMA, ',', '<')
edit_keymap.assign(p.K_PERIOD, '.', '>')
edit_keymap.assign(p.K_SLASH, '/', '?')
edit_keymap.assign(p.K_q, 'q', 'Q')
edit_keymap.assign(p.K_w, 'w', 'W')
edit_keymap.assign(p.K_e, 'e', 'E')
edit_keymap.assign(p.K_r, 'r', 'R')
edit_keymap.assign(p.K_t, 't', 'T')
edit_keymap.assign(p.K_y, 'y', 'Y')
edit_keymap.assign(p.K_u, 'u', 'U')
edit_keymap.assign(p.K_i, 'i', 'I')
edit_keymap.assign(p.K_o, 'o', 'O')
edit_keymap.assign(p.K_p, 'p', 'P')
edit_keymap.assign(p.K_a, 'a', 'A', Command(TextDisplay.select_all))
edit_keymap.assign(p.K_s, 's', 'S')
edit_keymap.assign(p.K_d, 'd', 'D')
edit_keymap.assign(p.K_f, 'f', 'F')
edit_keymap.assign(p.K_g, 'g', 'G')
edit_keymap.assign(p.K_h, 'h', 'H')
edit_keymap.assign(p.K_j, 'j', 'J')
edit_keymap.assign(p.K_k, 'k', 'K')
edit_keymap.assign(p.K_l, 'l', 'L')
edit_keymap.assign(p.K_z, 'z', 'Z')
edit_keymap.assign(p.K_x, 'x', 'X', Command(TextEditor.cut))
edit_keymap.assign(p.K_c, 'c', 'C', Command(TextEditor.copy))
edit_keymap.assign(p.K_v, 'v', 'V', Command(TextEditor.paste))
edit_keymap.assign(p.K_b, 'b', 'B')
edit_keymap.assign(p.K_n, 'n', 'N')
edit_keymap.assign(p.K_m, 'm', 'M')

code_keymap = Keymap()

code_keymap.assign(p.K_LEFT, Command(TextEditor.cursor_left), Command(TextEditor.highlight_left))
code_keymap.assign(p.K_RIGHT, Command(TextEditor.cursor_right), Command(TextEditor.highlight_right))
code_keymap.assign(p.K_DOWN, Command(TextEditor.cursor_down), Command(TextEditor.highlight_down))
code_keymap.assign(p.K_UP, Command(TextEditor.cursor_up), Command(TextEditor.highlight_up))
code_keymap.assign(p.K_BACKSPACE, Command(TextEditor.delete), Command(TextEditor.delete))
code_keymap.assign(p.K_TAB, Command(TextEditor.indent))
code_keymap.assign(p.K_RETURN, '\n')
code_keymap.assign(p.K_SPACE, ' ', ' ')
code_keymap.assign(p.K_1, '1', '!')
code_keymap.assign(p.K_2, '2', '@')
code_keymap.assign(p.K_3, '3', '#')
code_keymap.assign(p.K_4, '4', '$')
code_keymap.assign(p.K_5, '5', '%')
code_keymap.assign(p.K_6, '6', '^')
code_keymap.assign(p.K_7, '7', '&')
code_keymap.assign(p.K_8, '8', '*')
code_keymap.assign(p.K_9, '9', '(')
code_keymap.assign(p.K_0, '0', ')')
code_keymap.assign(p.K_BACKQUOTE, '`', '~')
code_keymap.assign(p.K_MINUS, '-', '_')
code_keymap.assign(p.K_EQUALS, '=', '+')
code_keymap.assign(p.K_LEFTBRACKET, '[', '{')
code_keymap.assign(p.K_RIGHTBRACKET, ']', '}')
code_keymap.assign(p.K_BACKSLASH, '\\', '|')
code_keymap.assign(p.K_SEMICOLON, ';', ':')
code_keymap.assign(p.K_QUOTE, "'", '"')
code_keymap.assign(p.K_COMMA, ',', '<')
code_keymap.assign(p.K_PERIOD, '.', '>')
code_keymap.assign(p.K_SLASH, '/', '?')
code_keymap.assign(p.K_q, 'q', 'Q')
code_keymap.assign(p.K_w, 'w', 'W')
code_keymap.assign(p.K_e, 'e', 'E')
code_keymap.assign(p.K_r, 'r', 'R', Command(CodeEditor.run, False, False))
code_keymap.assign(p.K_t, 't', 'T')
code_keymap.assign(p.K_y, 'y', 'Y')
code_keymap.assign(p.K_u, 'u', 'U')
code_keymap.assign(p.K_i, 'i', 'I')
code_keymap.assign(p.K_o, 'o', 'O')
code_keymap.assign(p.K_p, 'p', 'P')
code_keymap.assign(p.K_a, 'a', 'A', Command(TextEditor.select_all))
code_keymap.assign(p.K_s, 's', 'S')
code_keymap.assign(p.K_d, 'd', 'D')
code_keymap.assign(p.K_f, 'f', 'F')
code_keymap.assign(p.K_g, 'g', 'G')
code_keymap.assign(p.K_h, 'h', 'H')
code_keymap.assign(p.K_j, 'j', 'J')
code_keymap.assign(p.K_k, 'k', 'K')
code_keymap.assign(p.K_l, 'l', 'L')
code_keymap.assign(p.K_z, 'z', 'Z')
code_keymap.assign(p.K_x, 'x', 'X', Command(TextEditor.cut))
code_keymap.assign(p.K_c, 'c', 'C', Command(TextEditor.copy))
code_keymap.assign(p.K_v, 'v', 'V', Command(TextEditor.paste))
code_keymap.assign(p.K_b, 'b', 'B')
code_keymap.assign(p.K_n, 'n', 'N')
code_keymap.assign(p.K_m, 'm', 'M')