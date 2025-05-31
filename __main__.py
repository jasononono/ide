from script.requirement import dependency_check
dependency_check()


import pygame as p
import info

from script.editor import Screen


p.init()
screen = Screen()
clock = p.time.Clock()

while screen.execute:
    clock.tick(60)
    screen.refresh()
    p.display.set_caption(f"Beta IDE {info.version}")
p.quit()