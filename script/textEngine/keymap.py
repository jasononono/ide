import pygame as p

from script.textEngine.text import TextEditor
from script.textEngine.code import CodeEditor


class Key:
    def __init__(self, base = None, shift = None, ctrl = None, alt = None):
        self.base = base
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt


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


keymap = Keymap()

keymap.assign(p.K_LEFT, TextEditor.cursor_left, TextEditor.highlight_left)
keymap.assign(p.K_RIGHT, TextEditor.cursor_right, TextEditor.highlight_right)
keymap.assign(p.K_DOWN, TextEditor.cursor_down, TextEditor.highlight_down)
keymap.assign(p.K_UP, TextEditor.cursor_up, TextEditor.highlight_up)
keymap.assign(p.K_BACKSPACE, TextEditor.delete, TextEditor.delete)
keymap.assign(p.K_TAB, TextEditor.indent)
keymap.assign(p.K_RETURN, '\n')
keymap.assign(p.K_SPACE, ' ', ' ')
keymap.assign(p.K_1, '1', '!')
keymap.assign(p.K_2, '2', '@')
keymap.assign(p.K_3, '3', '#')
keymap.assign(p.K_4, '4', '$')
keymap.assign(p.K_5, '5', '%')
keymap.assign(p.K_6, '6', '^')
keymap.assign(p.K_7, '7', '&')
keymap.assign(p.K_8, '8', '*')
keymap.assign(p.K_9, '9', '(')
keymap.assign(p.K_0, '0', ')')
keymap.assign(p.K_BACKQUOTE, '`', '~')
keymap.assign(p.K_MINUS, '-', '_')
keymap.assign(p.K_EQUALS, '=', '+')
keymap.assign(p.K_LEFTBRACKET, '[', '{')
keymap.assign(p.K_RIGHTBRACKET, ']', '}')
keymap.assign(p.K_BACKSLASH, '\\', '|')
keymap.assign(p.K_SEMICOLON, ';', ':')
keymap.assign(p.K_QUOTE, "'", '"')
keymap.assign(p.K_COMMA, ',', '<')
keymap.assign(p.K_PERIOD, '.', '>')
keymap.assign(p.K_SLASH, '/', '?')
keymap.assign(p.K_q, 'q', 'Q')
keymap.assign(p.K_w, 'w', 'W')
keymap.assign(p.K_e, 'e', 'E')
keymap.assign(p.K_r, 'r', 'R', CodeEditor.run)
keymap.assign(p.K_t, 't', 'T')
keymap.assign(p.K_y, 'y', 'Y')
keymap.assign(p.K_u, 'u', 'U')
keymap.assign(p.K_i, 'i', 'I')
keymap.assign(p.K_o, 'o', 'O')
keymap.assign(p.K_p, 'p', 'P')
keymap.assign(p.K_a, 'a', 'A', TextEditor.select_all)
keymap.assign(p.K_s, 's', 'S')
keymap.assign(p.K_d, 'd', 'D')
keymap.assign(p.K_f, 'f', 'F')
keymap.assign(p.K_g, 'g', 'G')
keymap.assign(p.K_h, 'h', 'H')
keymap.assign(p.K_j, 'j', 'J')
keymap.assign(p.K_k, 'k', 'K')
keymap.assign(p.K_l, 'l', 'L')
keymap.assign(p.K_z, 'z', 'Z')
keymap.assign(p.K_x, 'x', 'X', TextEditor.cut)
keymap.assign(p.K_c, 'c', 'C', TextEditor.copy)
keymap.assign(p.K_v, 'v', 'V', TextEditor.paste)
keymap.assign(p.K_b, 'b', 'B')
keymap.assign(p.K_n, 'n', 'N')
keymap.assign(p.K_m, 'm', 'M')