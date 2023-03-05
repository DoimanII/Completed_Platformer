import time

import pygame as pg

keys = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, 'F3':True}

WIN_SIZE = (1280, 720)
SCALE = 4
screen = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN, vsync=1) # , pg.FULLSCREEN
WIN_RES = (screen.get_size()[0] // SCALE, screen.get_size()[1] // SCALE)
display = pg.Surface(WIN_RES)

clock = pg.time.Clock()
FPS = 60
timer = 0

animation_database = {}
animation_higher_database = {}

tile_database = {
    0:pg.image.load('assets/sprites/tileset/ground_tiles/grass_16x16.png').convert_alpha(), # TileSet
    1:pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x16.png').convert_alpha(),
    2:pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x32.png').convert_alpha(),
    9:pg.image.load('assets/sprites/tileset/ground_tiles/BIG_grass_128x128.png').convert_alpha(),

    3:pg.image.load('assets/sprites/tileset/ground_tiles/dirt_16x16.png').convert_alpha(),
    4:pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x16.png').convert_alpha(),
    5:pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x32.png').convert_alpha(),
    10:pg.image.load('assets/sprites/tileset/ground_tiles/BIG_dirt_128x128.png').convert_alpha(),

    6:pg.image.load('assets/sprites/tileset/world_objects/little_tree_16x16.png').convert_alpha(), # World Obj
    8:pg.image.load('assets/sprites/tileset/world_objects/plant_16x16.png').convert_alpha(),


    11:pg.image.load('assets/sprites/spikes.png').convert_alpha(), # Entity sprites
    7: pg.image.load('assets/sprites/tileset/world_objects/bush_16x16.png').convert_alpha(),
    12: pg.image.load('assets/sprites/tileset/world_objects/bush_eaten_16x16.png').convert_alpha(),

                 }

