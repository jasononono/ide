import pygame as p
import pyperclip
import settings
from script.utility import Object
from assets import palette

from script.textEngine.font import Font
from script.textEngine.cursor import Cursor
from script.textEngine.action import ViewAction, EditAction


class TextEffect:
    def __init__(self, opacity = 255, colour = None, highlight = 0):
        self.opacity = opacity
        self.colour = colour
        self.highlight = highlight


class StaticDisplay(Object):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white,
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(position, size, True)
        self.text = text
        self.background = background
        self.foreground = foreground

        self.font = Font(font_size, font)
        self.margin = margin
        self.spacing = spacing
        self.offset = [0, 0]

        self.map = []
        self.charMap = []

    def refresh(self, parent, event):
        self.rect.refresh(parent.rect)

        self.surface.fill(self.background)
        self.display_text()
        parent.display(self.surface, self.rect)

    def write(self, text):
        self.text = text

    def display_char(self, char, line, pointer, position):
        if char != '\n':
            surface = self.font.render(char, self.foreground)
            self.display(surface, (pointer - self.offset[0],
                                   self.margin[1] + line * (self.font.height + self.spacing[1]) - self.offset[1]))

    def display_text(self):
        self.map = [[]]
        self.charMap = [[]]
        pointer = self.margin[0]
        line = 0

        for n, i in enumerate(self.text):
            self.display_char(i, line, pointer, n)
            if i == '\n':
                self.map.append([])
                self.charMap.append([])
                pointer = self.margin[0]
                line += 1
            else:
                pointer += self.font.glyphs[i] + self.spacing[0]
                self.map[line].append(pointer)
                self.charMap[line].append(i)

    def get_location(self, **kwargs):
        name, value = list(kwargs.items())[0]
        if name == "position":
            return self.get_location(coordinate = self.get_coordinate(position = value))

        if name == "coordinate":
            return ((self.margin[0] if value[0] == 0 else self.map[value[1]][value[0] - 1]),
                   self.margin[1] + value[1] * (self.font.height + self.spacing[1]))
        return None

    def get_position(self, **kwargs):
        name, value = list(kwargs.items())[0]
        absolute = True if "absolute" in kwargs.keys() and kwargs["absolute"] is True else False
        if name == "location":
            return self.get_position(coordinate = self.get_coordinate(location = value, absolute = absolute))

        if name == "coordinate":
            column = max(value[0], 0)
            row = max(value[1], 0)
            pos = sum([len(i) for i in self.map[:row]]) + row + min(len(self.map[row]), column)
            return min(len(self.text), max(0, pos))
        return None

    def get_coordinate(self, **kwargs):
        name, value = list(kwargs.items())[0]
        absolute = True if "absolute" in kwargs.keys() and kwargs["absolute"] is True else False
        if name == "location":
            row = ((value[1] + self.offset[1] - self.margin[1] - (self.rect.abs.y if absolute else 0)) /
                   (self.spacing[1] + self.font.height))
            row = int(max(min(row, len(self.map) - 1), 0))

            if len(self.charMap[row]) == 0:
                return 0, row
            pointer = 0
            column = None
            for i in range(len(self.charMap[row])):
                pointer += (0 if i == 0 else self.font.glyphs[self.charMap[row][i - 1]] / 2 + self.spacing[0])
                pointer += self.font.glyphs[self.charMap[row][i]] / 2
                if value[0] + self.offset[0] - self.margin[0] - (self.rect.abs.x if absolute else 0) < pointer:
                    column = i
                    break

            if column is None:
                column = len(self.map[row])
            column = round(max(min(column, len(self.map[row])), 0))
            return column, row

        if name == "position":
            if value < 0:
                return 0, 0
            total = 0
            for i, j in enumerate(self.map):
                total += len(j) + 1
                if value < total:
                    return value - total + len(j) + 1, i
            return self.get_coordinate(position = len(self.text))
        return None


class FancyDisplay(StaticDisplay):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white,
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(text, position, size, background, foreground, font, font_size, margin, spacing)
        self.textEffects = []
        self.write(text)

    def write(self, text):
        if len(self.textEffects) > len(text):
            self.textEffects = self.textEffects[:len(text)]
        else:
            for _ in range(len(text) - len(self.textEffects)):
                self.textEffects.append(TextEffect())
        self.text = text

    def display_char(self, char, line, pointer, position):
        if settings.smoothText:
            self.textEffects[position].opacity = min(255, self.textEffects[position].opacity + settings.textFadeIn)

        if char != '\n':
            colour = self.foreground if self.textEffects[position].colour is None else self.textEffects[position].colour
            surface = self.font.render(char, colour)
            if settings.smoothText:
                surface.set_alpha(self.textEffects[position].opacity)
            self.display(surface, (pointer - self.offset[0],
                                   self.margin[1] + line * (self.font.height + self.spacing[1]) - self.offset[1]))


class TextDisplay(FancyDisplay):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(text, position, size, background, foreground, font, font_size, margin, spacing)
        from script.textEngine.keymap import view_keymap
        self.action = ViewAction(view_keymap)
        self.cursor = Cursor()
        self.highlight = Cursor()
        self.highlightForeground = [(i + j) / 2 for i, j in zip(highlight_foreground, background)]

    def display_char(self, char, line, pointer, position):
        highlighted = int(self.highlight.position is not None and min(self.cursor.position, self.highlight.position) <=
                          position < max(self.cursor.position, self.highlight.position))
        y_location = self.margin[1] + line * (self.font.height + self.spacing[1])

        surface = p.Surface((self.font.glyphs[char] + self.spacing[0], self.font.height + self.spacing[1]))
        surface.fill(self.highlightForeground)

        if settings.smoothHighlight:
            self.textEffects[position].highlight = (min(255, self.textEffects[position].highlight +
                                                        settings.highlightFadeIn) if highlighted else
                                                    max(0, self.textEffects[position].highlight -
                                                        settings.highlightFadeIn))
            surface.set_alpha(self.textEffects[position].highlight)
            self.display(surface, (pointer - self.offset[0], y_location - self.offset[1]))
        elif highlighted:
            self.display(surface, (pointer - self.offset[0], y_location - self.offset[1]))
        super().display_char(char, line, pointer, position)

    def refresh(self, parent, event):
        self.action.refresh(self, event)
        super().refresh(parent, event)


class TextEditor(TextDisplay):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0)):
        super().__init__(text, position, size, background, foreground, highlight_foreground,
                         font, font_size, margin, spacing)
        from script.textEngine.keymap import edit_keymap
        self.action = EditAction(edit_keymap)
        self.cursor.position = 0

    def display_char(self, char, line, pointer, position):
        super().display_char(char, line, pointer, position)

    def display_text(self):
        super().display_text()
        if self.highlight.position == self.cursor.position:
            self.highlight.position = None
        if self.highlight.position is None:
            self.cursor.refresh(self)

    def refresh(self, parent, event):
        super().refresh(parent, event)
        if self.valid_mouse_position(event.mousePosition):
            p.mouse.set_cursor(p.SYSTEM_CURSOR_IBEAM)

    def append(self, text):
        if self.highlight.position is None:
            self.text = self.text[:self.cursor.position] + text + self.text[self.cursor.position:]
            for i in range(self.cursor.position, self.cursor.position + len(text)):
                self.textEffects.append(TextEffect())
                if settings.smoothText:
                    self.textEffects[i].opacity = 0
            self.cursor.position += len(text)

        else:
            start = min(self.cursor.position, self.highlight.position)
            self.text = (self.text[:start] + text + self.text[max(self.cursor.position, self.highlight.position):])
            for i in range(start, start + len(text)):
                self.textEffects.append(TextEffect())
                if settings.smoothText:
                    self.textEffects[i].opacity = 0
            self.cursor.position = start + len(text)
            self.cursor.location = None
            self.highlight.position = None

    def delete(self):
        if self.highlight.position is not None:
            start = min(self.cursor.position, self.highlight.position)
            self.text = (self.text[:start] + self.text[max(self.cursor.position, self.highlight.position):])
            if settings.smoothHighlight:
                for i in range(start, start + abs(self.highlight.position - self.cursor.position)):
                    self.textEffects[i].highlight = 0
            self.cursor.position = start
            self.cursor.location = None
            self.highlight.position = None

        elif self.cursor.position > 0:
            self.text = self.text[:self.cursor.position - 1] + self.text[self.cursor.position:]
            self.cursor.position -= 1

    def cursor_left(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
            self.cursor.location = None
        elif self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def cursor_right(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
            self.cursor.location = None
        elif self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def cursor_down(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (len(self.text) if row == len(self.map) - 1 else
                                self.get_position(location = (location[0],
                                                              location[1] + self.font.height + self.spacing[1])))
        self.cursor.blink = 0

    def cursor_up(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (0 if row == 0 else
                                self.get_position(location = (location[0],
                                                              location[1] - self.font.height - self.spacing[1])))
        self.cursor.blink = 0

    def highlight_left(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def highlight_right(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def highlight_down(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (len(self.text) if row == len(self.map) - 1 else
                                self.get_position(location = (location[0],
                                                              location[1] + self.font.height + self.spacing[1])))
        self.cursor.blink = 0

    def highlight_up(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (0 if row == 0 else
                                self.get_position(location = (location[0],
                                                              location[1] - self.font.height - self.spacing[1])))
        self.cursor.blink = 0

    def indent(self):
        self.append("    ")

    def select_all(self):
        self.highlight.position = 0
        self.cursor.position = len(self.text)

    def copy(self):
        if self.highlight.position is not None:
            pyperclip.copy(self.text[min(self.cursor.position, self.highlight.position):
                                     max(self.cursor.position, self.highlight.position)])

    def paste(self):
        self.append(pyperclip.paste())

    def cut(self):
        self.copy()
        self.delete()