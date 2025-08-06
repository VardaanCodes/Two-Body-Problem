import pygame as pg
import numpy as np
pg.init()

width, height = 800, 600

entry_screen_bg = pg.image.load("entry_screen_bg.png")

screen = pg.display.set_mode((width, height))
pg.display.set_caption("Two-Body Problem Simulation")

link = "entry-screen/"



running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    # Update the display
    pg.display.flip()
    # Cap the frame rate
    pg.time.Clock().tick(60)
# Quit Pygame
pg.quit()
