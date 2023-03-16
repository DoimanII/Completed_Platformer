import pygame as pg
import sys, time

import Engine
from Debug import debug
from Settings import *
from assets.levels.TheFirstLevel import TheFirstLevel
from assets.levels.Sample import Sample

pg.init()

Engine.load_animation('assets/')
game_levels = {'TheFirst': TheFirstLevel(),
                'Sample': Sample(),
               }
state = 'TheFirst'


messager = Engine.GUI()
loading_timer = 4
while True:
    dt = clock.tick(FPS) / 1000
    timer += dt
    display.fill((134, 212, 229))

    # Load game
    if int(timer) > loading_timer:
        game_levels[state].play(display, dt)
    else:
        pg.draw.rect(display, 'red', ((50, 100), (25*timer, 10)))

    # transform win_res
    surf = pg.transform.scale(display, WIN_SIZE)
    screen.blit(surf, (0, 0))

    # show F3_info
    if keys['F3']:
        debug(f'FPS: {int(clock.get_fps())} | player_rect: {game_levels[state].player.get_rect()}', screen)
        debug(f'collision top/bottom:{game_levels[state].player.collision["top"], game_levels[state].player.collision["bottom"]}', screen, (15,45))
        debug(
            f'collision left/right:{game_levels[state].player.collision["left"], game_levels[state].player.collision["right"]}',
            screen, (15, 75))

    # Render text
    if int(timer) > loading_timer+1:
        messager.message(game_levels[state].text)

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_F1:
                pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN, vsync=1)
            if event.key == pg.K_F2:
                pg.display.set_mode(WIN_SIZE, vsync=1)
            if event.key == pg.K_F3:
                keys['F3'] = True if keys['F3'] == False else False

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

