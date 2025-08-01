import pygame as p
import math
import pyperclip
import settings
from script.utility import Object
from assets import palette

from script.textEngine.font import Font
from script.textEngine.cursor import Cursor
from script.textEngine.action import ViewAction, EditAction
from script.textEngine.scroll import Scroll


# OFFSET BEHAVIOUR NOT DEFINED FOR CURSOR: try printing a lot of things and highlighting in output pane


class TextEffect:
    def __init__(self, opacity = 255, colour = None, highlight = 0):
        self.opacity = opacity
        self.colour = colour
        self.highlight = highlight


class StaticDisplay(Object):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white,
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0), offset = None):
        super().__init__(position, size, True)
        self.text = text
        self.background = background
        self.foreground = foreground

        self.font = Font(font_size, font)
        self.margin = margin
        self.spacing = spacing
        self.offset = offset or [0, 0]

        self.map = []
        self.charMap = []
        self.charMax = [0, 0]

    def update(self, parent, event):
        self.display_text(event)

    def refresh(self, parent, event):
        self.rect.refresh(parent.rect)

        self.surface.fill(self.background)
        self.update(parent, event)
        parent.display(self.surface, self.rect)

    def write(self, text):
        self.text = text

    def append(self, text):
        self.text += text

    def erase(self):
        self.text = ""

    def get_line(self, line):
        return self.margin[1] + line * (self.font.height + self.spacing[1])

    def display_char(self, char, line, pointer, position):
        if char != '\n':
            surface = self.font.render(char, self.foreground)
            self.display(surface, (pointer - self.offset[0], line - self.offset[1]))

    def display_text(self, event):
        self.map = [[]]
        self.charMap = [[]]
        self.charMax = [0, 0]
        pointer = self.margin[0]
        line = 0

        for n, i in enumerate(self.text):
            line_location = self.get_line(line)
            self.display_char(i, line_location, pointer, n)

            if i == '\n':
                self.charMax[0] = max(self.charMax[0], (self.map[-1][-1] if len(self.map[-1]) > 0 else 0))
                self.map.append([])
                self.charMap.append([])
                pointer = self.margin[0]
                line += 1
            else:
                pointer += self.font.glyphs[i] + self.spacing[0]
                self.map[line].append(pointer)
                self.charMap[line].append(i)

        self.charMax[0] = self.margin[0] + max(self.charMax[0], self.map[-1][-1] if len(self.map[-1]) > 0 else 0)
        self.charMax[1] = self.get_line(line + 1) + self.margin[1]

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
        offset = False if "offset" in kwargs.keys() and kwargs["offset"] is False else True
        
        if name == "location":
            return self.get_position(coordinate = self.get_coordinate(location = value,
                                                                      absolute = absolute, offset = offset))

        if name == "coordinate":
            column = max(value[0], 0)
            row = max(value[1], 0)
            pos = sum([len(i) for i in self.map[:row]]) + row + min(len(self.map[row]), column)
            return min(len(self.text), max(0, pos))
        return None

    def get_coordinate(self, **kwargs):
        name, value = list(kwargs.items())[0]
        absolute = True if "absolute" in kwargs.keys() and kwargs["absolute"] is True else False
        offset = False if "offset" in kwargs.keys() and kwargs["offset"] is False else True
        
        if name == "location":
            row = ((value[1] + (self.offset[1] if offset else 0) - self.margin[1] -
                    (self.rect.abs.y if absolute else 0)) / (self.spacing[1] + self.font.height))
            row = int(max(min(row, len(self.map) - 1), 0))

            if len(self.charMap[row]) == 0:
                return 0, row
            pointer = 0
            column = None
            for i in range(len(self.charMap[row])):
                pointer += (0 if i == 0 else self.font.glyphs[self.charMap[row][i - 1]] / 2 + self.spacing[0])
                pointer += self.font.glyphs[self.charMap[row][i]] / 2
                if (value[0] + (self.offset[0] if offset else 0) - self.margin[0] -
                    (self.rect.abs.x if absolute else 0) < pointer):
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
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0), real_size = None, offset = None):
        super().__init__(text, position, size, background, foreground, font, font_size, margin, spacing, offset)
        self.text = text
        self.textEffects = []
        self.realSize = real_size
        self.resize_effects()

        self.scrollx = Scroll(self, (0, self.rect.height - 7), 0)
        self.scrolly = Scroll(self, (self.rect.width - 7, 0), 1)
        self.scrolling = False

    def resize_effects(self):
        if len(self.textEffects) < len(self.text):
            for i in range(len(self.text) - len(self.textEffects)):
                self.textEffects.append(TextEffect())

    def update(self, parent, event):
        super().update(parent, event)
        self.scrolling = self.scrollx.refresh(self, event)
        self.scrolling = self.scrolly.refresh(self, event) or self.scrolling

    def append(self, text, colour = None):
        old_length = len(self.text)
        self.text += text
        self.resize_effects()
        for i in range(old_length, old_length + len(text)):
            self.textEffects[i].colour = colour

    def write(self, text):
        self.text = text
        self.resize_effects()

    def erase(self):
        self.text = ""
        self.resize_effects()

    def display_char(self, char, line, pointer, position):
        if settings.smoothText:
            self.textEffects[position].opacity = min(255, self.textEffects[position].opacity + settings.textFadeIn)

        if char != '\n':
            colour = self.foreground if self.textEffects[position].colour is None else self.textEffects[position].colour
            surface = self.font.render(char, colour)
            if settings.smoothText:
                surface.set_alpha(self.textEffects[position].opacity)
            self.display(surface, (pointer - self.offset[0], line - self.offset[1]))


class TextDisplay(FancyDisplay):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0),
                 real_size = None, offset = None):
        super().__init__(text, position, size, background, foreground, font, font_size, margin, spacing, real_size,
                         offset)
        from script.textEngine.keymap import view_keymap
        self.action = ViewAction(view_keymap)
        self.cursor = Cursor()
        self.highlight = Cursor()
        self.highlightForeground = [(i + j) / 2 for i, j in zip(highlight_foreground, background)]
        self.targetOffset = None
        self.fixingOffset = False
        self.to_end = False

    def write(self, text):
        super().write(text)
        self.cursor.position = None
        self.highlight.position = None
        self.to_end = True

    def erase(self):
        super().erase()
        self.cursor.position = None
        self.highlight.position = None
        self.to_end = True

    def display_char(self, char, line, pointer, position):
        highlighted = int(self.highlight.position is not None and min(self.cursor.position, self.highlight.position) <=
                          position < max(self.cursor.position, self.highlight.position))

        surface = p.Surface((self.font.glyphs[char] + self.spacing[0], self.font.height + self.spacing[1]))
        surface.fill(self.highlightForeground)

        if settings.smoothHighlight:
            self.textEffects[position].highlight = (min(settings.highlightOpacity,
                                                        self.textEffects[position].highlight + settings.highlightFadeIn)
                                                    if highlighted else max(0, self.textEffects[position].highlight -
                                                                               settings.highlightFadeIn))
            surface.set_alpha(self.textEffects[position].highlight)
            self.display(surface, (pointer - self.offset[0], line - self.offset[1]))
        elif highlighted:
            self.display(surface, (pointer - self.offset[0], line - self.offset[1]))
        super().display_char(char, line, pointer, position)

    def fit_screen(self, cursor):
        if cursor.position is None:
            return
        target_location = (cursor.targetLocation[0], cursor.targetLocation[1] + self.font.height)

        for i in range(2):
            if target_location[i] >= self.offset[i] + self.rect.size[i] - 10:
                self.target_offset(i, target_location[i] - self.rect.size[i] + 10)
            elif target_location[i] <= self.offset[i] + 10 + self.font.height:
                self.target_offset(i, target_location[i] - 10 - self.font.height)
            if self.offset[i] + self.rect.size[i] > self.realSize[i]:
                self.target_offset(i, max(0, self.realSize[i] - self.rect.size[i]))

    def update(self, parent, event):
        super().update(parent, event)

        self.realSize = self.charMax

        if not self.cursor.moving:
            self.fixingOffset = False

        if self.action.refreshScroll:
            self.fixingOffset = True
            self.targetOffset = self.offset.copy()

        if self.fixingOffset:
            self.fit_screen(self.cursor)
        if self.offset == self.targetOffset:
            self.targetOffset = None
            self.fixingOffset = False

        if self.targetOffset:
            if settings.smoothCursor:
                for i in range(2):
                    if self.offset[i] < self.targetOffset[i]:
                        self.offset[i] = math.ceil((self.offset[i] + self.targetOffset[i]) / 2)
                    else:
                        self.offset[i] = math.floor((self.offset[i] + self.targetOffset[i]) / 2)
            else:
                self.offset = self.targetOffset.copy()

        if self.to_end:
            self.targetOffset = [max(0, self.realSize[i] - self.rect.size[i]) for i in range(2)]
            self.to_end = False

        if event.active is self:
            parent.draw_rect(palette.dark3,
                             (self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2))

    def target_offset(self, side, *args):
        if side == 0:
            self.targetOffset[0] = args[0]
        elif side == 1:
            self.targetOffset[1] = args[0]
        else:
            self.targetOffset = [args[0], args[1]]

    def refresh(self, parent, event):
        super().refresh(parent, event)
        self.action.refresh(self, event)

    def select_all(self):
        self.highlight.position = 0
        self.cursor.position = len(self.text)


class TextEditor(TextDisplay):
    def __init__(self, text = "", position = (0, 0), size = (400, 300),
                 background = palette.dark0, foreground = palette.white, highlight_foreground = (100, 200, 255),
                 font = None, font_size = 15, margin = (0, 0), spacing = (0, 0), real_size = None, offset = None):
        super().__init__(text, position, size, background, foreground, highlight_foreground,
                         font, font_size, margin, spacing, real_size, offset)
        from script.textEngine.keymap import edit_keymap
        self.action = EditAction(edit_keymap)
        self.cursor.position = 0

    def display_text(self, event):
        super().display_text(event)
        if self.highlight.position == self.cursor.position:
            self.highlight.position = None
        self.cursor.refresh(self)
        self.highlight.refresh(self)
        if event.active is self and self.highlight.position is None:
            self.cursor.display(self)

    def refresh(self, parent, event):
        if event.active is self and self.valid_mouse_position(event.mousePosition):
            event.cursor = p.SYSTEM_CURSOR_IBEAM
        super().refresh(parent, event)

    def insert(self, text):
        self.text = self.text[:self.cursor.position] + text + self.text[self.cursor.position:]

        for i in range(self.cursor.position, self.cursor.position + len(text)):
            if len(self.textEffects) <= len(self.text):
                self.textEffects.insert(i, TextEffect())
            else:
                self.textEffects[i] = TextEffect()
        self.cursor.position += len(text)

    def append(self, text, colour = None):
        if self.highlight.position is None:
            self.text = self.text[:self.cursor.position] + text + self.text[self.cursor.position:]

            for i in range(self.cursor.position, self.cursor.position + len(text)):
                if len(self.textEffects) <= len(self.text):
                    self.textEffects.insert(i, TextEffect())
                else:
                    self.textEffects[i] = TextEffect()
                if settings.smoothText:
                    self.textEffects[i].opacity = 0
                self.textEffects[i].colour = colour
            self.cursor.position += len(text)

        else:
            self.delete()
            self.insert(text)

    def delete(self):
        if self.highlight.position is not None:
            start = min(self.cursor.position, self.highlight.position)
            self.text = (self.text[:start] + self.text[max(self.cursor.position, self.highlight.position):])
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
                                                              location[1] + self.font.height + self.spacing[1]),
                                                  offset = False))
        self.cursor.blink = 0

    def cursor_up(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (0 if row == 0 else
                                self.get_position(location = (location[0],
                                                              location[1] - self.font.height - self.spacing[1]),
                                                  offset = False))
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
                                                              location[1] + self.font.height + self.spacing[1]),
                                                  offset = False))
        self.cursor.blink = 0

    def highlight_up(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinate(position = self.cursor.position)
        location = self.get_location(coordinate = (column, row))
        self.cursor.position = (0 if row == 0 else
                                self.get_position(location = (location[0],
                                                              location[1] - self.font.height - self.spacing[1]),
                                                  offset = False))
        self.cursor.blink = 0

    def indent(self):
        self.append("    ")

    def copy(self):
        if self.highlight.position is not None:
            pyperclip.copy(self.text[min(self.cursor.position, self.highlight.position):
                                     max(self.cursor.position, self.highlight.position)])

    def paste(self):
        self.append(pyperclip.paste())

    def cut(self):
        self.copy()
        self.delete()