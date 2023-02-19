import pygame as pg
import sys

import Engine
from Debug import debug
from Settings import *
from assets.levels.TestLevel import TestLevel
from assets.levels.Sample import Sample
pg.init()

Engine.load_animation('assets/')
game_levels = {'Test': TestLevel(),
               'Sample': Sample()}
state = 'Sample'

while True:
    dt = clock.tick(FPS) / 1000
    display.fill((134, 212, 229))

    game_levels[state].play(display, dt)
    debug(f'{int(clock.get_fps())} | {Engine.get_mouse_pos()}', display)

    surf = pg.transform.scale(display, WIN_SIZE)
    screen.blit(surf, (0, 0))
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

            if event.key == pg.K_LEFT or event.key == pg.K_a:  # Left
                keys['left'] = True
            if event.key == pg.K_RIGHT or event.key == pg.K_d:  # Right
                keys['right'] = True
            if event.key == pg.K_UP or event.key == pg.K_w:  # Up
                keys['up'] = True
            if event.key == pg.K_DOWN or event.key == pg.K_s:  # Down
                keys['down'] = True

            if event.key == pg.K_e:
                keys['action'] = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_a:  # Left
                keys['left'] = False
            if event.key == pg.K_RIGHT or event.key == pg.K_d:  # Right
                keys['right'] = False
            if event.key == pg.K_UP or event.key == pg.K_w:  # Up
                keys['up'] = False
            if event.key == pg.K_DOWN or event.key == pg.K_s:  # Down
                keys['down'] = False

            if event.key == pg.K_e:
                keys['action'] = False
