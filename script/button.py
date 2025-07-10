from script.utility import Object
from assets import palette

class Button(Object):
    def __init__(self, position, size, active_on_hover = True,
                 colour = palette.dark2, active_colour = palette.dark3):
        super().__init__(position, size)
        self.activeOnHover = active_on_hover
        self.colour = colour
        self.activeColour = active_colour

        self.status = True
        self.active = False
        self.hover = False
        self.pressed = False

    def refresh(self, parent, event):
        self.rect.refresh(parent.rect)
        if self.valid_mouse_position(event.mousePosition):
            self.hover = True
            if event.mouse_down():
                self.pressed = True
        else:
            self.hover = False

        if self.status and (self.active or self.pressed or (self.hover and self.activeOnHover)):
            self.fill(self.activeColour)
        else:
            self.fill(self.colour)
        parent.display(self.surface, self.rect)

        if event.mouse_up():
            self.pressed = False
            if self.status and self.hover:
                return True
        return False