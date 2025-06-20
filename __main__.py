from script.requirement import dependency_check
dependency_check()


import pygame as p
import settings

from script.screen import Screen


p.init()
screen = Screen()
clock = p.time.Clock()

p.display.set_caption(f"Beta IDE {settings.version}")

while screen.execute:
    clock.tick(60)
    screen.refresh()

    p.display.flip()
    
p.quit()
