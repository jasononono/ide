import pygame as p


def get_modifier(keys):
    shift = keys[p.K_LSHIFT] or keys[p.K_RSHIFT]
    ctrl = keys[p.K_LCTRL] or keys[p.K_RCTRL] or keys[p.K_LMETA] or keys[p.K_RMETA]
    alt = keys[p.K_LALT] or keys[p.K_RALT]

    if shift + ctrl + alt > 1:
        return None
    if shift:
        return "shift"
    if ctrl:
        return "ctrl"
    if alt:
        return "alt"
    return None


class Action:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.keyPressed = None
        self.keyCooldown = 0
        self.modifier = None
        self.mouseDown = False

    def press(self, parent):
        key = self.keyboard.retrieve(self.keyPressed, self.modifier)
        if key is None:
            return
        if callable(key):
            key(parent)
        else:
            parent.append(key)

    def refresh(self, parent, event):
        self.modifier = get_modifier(event.key)

        key = event.key_down()
        if key in self.keyboard.map.keys():
            self.keyPressed = key
            self.press(parent)
            self.keyCooldown = 30
        if event.key_up(self.keyPressed):
            self.keyPressed = None
        if event.mouse_down():
            """
            if self.boundary(event.mousePos):
                coord = self.parent.get_mouse_coordinates(event.mousePos)
                self.mouseDown = True
                if self.modifier == "shift":
                    if self.parent.highlight.position is None:
                        self.parent.highlight.position = self.parent.cursor.py.position
                    self.parent.cursor.py.position = self.parent.get_position(coord)
                else:
                    self.parent.cursor.py.position = self.parent.get_position(coord)
                    self.parent.cursor.py.blink = 0
                    self.parent.highlight.position = None
            """

        if self.keyPressed is not None:
            if self.keyCooldown > 0:
                self.keyCooldown -= 1
            else:
                self.press(parent)
                self.keyCooldown = 3

        """
        if not event.mouse[0]:
            self.mouseDown = False
        if self.mouseDown:
            coord = self.parent.get_mouse_coordinates(event.mousePos)
            position = self.parent.get_position(coord)
            if position != self.parent.cursor.py.position:
                if position == self.parent.highlight.position:
                    self.parent.highlight.position = None
                elif self.parent.highlight.position is None:
                    self.parent.highlight.position = self.parent.cursor.py.position
                self.parent.cursor.py.position = position
                self.parent.cursor.py.blink = 0
        """