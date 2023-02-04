import pygame as pg

M = 1
WIN_SIZE, WIN_RES = (800, 600), (800//M, 600//M)
FPS = 60


keys = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, }

screen = pg.display.set_mode(WIN_SIZE)
display = pg.Surface(WIN_RES)
clock = pg.time.Clock()

animation_database = {}
animation_higher_database = {}