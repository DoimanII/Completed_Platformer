import random

import pygame as pg
import sys, time

import Engine
from Debug import debug
from Settings import *
from assets.levels.TheFirstLevel import TheFirstLevel
from assets.levels.TheSecondLevel import TheSecondLevel
from assets.levels.Sample import Sample
from assets.levels.MainMenu import MainMenu
from assets.levels.TheThird import TheThird

from SUJA import TEST

pg.init()

Engine.load_animation('assets/')
game_levels = {'TheFirst': TheFirstLevel(),
               'TheSecond': TheSecondLevel(),
               'TheThird': TheThird(),
               'Sample': Sample(),
               'main_menu': MainMenu(),
               'Test': TEST(),
               }

messager = Engine.GUI()
loading_timer = 2

state = 'main_menu'
last_state = None


def state_manager():
    global state, last_state, game_levels
    if game_levels[state].change_level_to:
        last_state = state
        state = game_levels[state].change_level_to
        game_levels[state].change_level_to = None

        game_levels['main_menu'].change_level_to = None

    if state == 'main_menu' and game_levels[state].new_game:  # Так себе решение обнуления игры
        game_levels['TheFirst'] = TheFirstLevel()
        game_levels['TheSecond'] = TheSecondLevel()

        game_levels[state].new_game = False
        state = 'TheFirst'

#pg.mixer.music.play(loops=-1)
while True:
    state_manager()
    dt = clock.tick(FPS) / 1000
    timer += dt
    display.fill(BACKGROUND_COLOR)

    # Load game
    if int(timer) > loading_timer:
        game_levels[state].play(display, dt, last_state)
    else:
        pg.draw.rect(display, 'red', ((50, 100), (25 * timer, 10)))

    # transform win_res
    surf = pg.transform.scale(display, WIN_SIZE)
    screen.blit(surf, (0, 0))

    # show F3_info
    if keys['F3']:
        debug(f'FPS: {int(clock.get_fps())} | E - action, Space - jump, WASD - move, F1 - Fullscreen, F2 - window', screen)
        debug(
            f'При получение урона кусты с ягодой можно кушать, нажав кнопку Е',
            screen, (15, 45))


    # Render text
    if int(timer) > loading_timer:
        messager.message(game_levels[state].text)

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if state == 'main_menu':
                    pg.quit()
                    sys.exit()
                else:
                    last_state = state
                    state = 'main_menu'

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
