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
            if parent.valid_mouse_position(event.mousePosition):
                coordinate = parent.get_coordinate(location = event.mousePosition)
                print(coordinate)
                self.mouseDown = True
                if self.modifier == "shift":
                    if parent.highlight.position is None:
                        parent.highlight.position = parent.cursor.position
                else:
                    parent.cursor.blink = 0
                    parent.highlight.position = None
                parent.cursor.position = parent.get_position(coordinate = coordinate)

        if event.mouse_up():
            self.mouseDown = False

        if self.keyPressed is not None:
            if self.keyCooldown > 0:
                self.keyCooldown -= 1
            else:
                self.press(parent)
                self.keyCooldown = 3

        if self.mouseDown:
            coordinate = parent.get_coordinate(location = event.mousePosition)
            position = parent.get_position(coordinate = coordinate)
            if position != parent.cursor.position:
                if position == parent.highlight.position:
                    parent.highlight.position = None
                elif parent.highlight.position is None:
                    parent.highlight.position = parent.cursor.position
                parent.cursor.position = position
                parent.cursor.blink = 0