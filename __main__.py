import pygame as p

from editor import Screen

p.init()
screen = Screen()
clock = p.time.Clock()

while screen.execute:
    clock.tick(60)
    screen.refresh()
p.quit()