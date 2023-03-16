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
    'grass':pg.image.load('assets/sprites/tileset/ground_tiles/grass_16x16.png').convert_alpha(), # TileSet 0
    'grass32x16':pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x16.png').convert_alpha(), # 1
    'grass32x32':pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x32.png').convert_alpha(), # 2
    'grass128x128':pg.image.load('assets/sprites/tileset/ground_tiles/BIG_grass_128x128.png').convert_alpha(), # 9

    'dirt':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_16x16.png').convert_alpha(), # 3
    'dirt32x16':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x16.png').convert_alpha(), # 4
    'dirt32x32':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x32.png').convert_alpha(), # 5
    'dirt128x128':pg.image.load('assets/sprites/tileset/ground_tiles/BIG_dirt_128x128.png').convert_alpha(), # 10

    'little_tree':pg.image.load('assets/sprites/tileset/world_objects/little_tree_16x16.png').convert_alpha(), # World Obj 6
    'plant':pg.image.load('assets/sprites/tileset/world_objects/plant_16x16.png').convert_alpha(), # 8


    'spikes':pg.image.load('assets/sprites/spikes.png').convert_alpha(), # Entity sprites 11
    'bush': pg.image.load('assets/sprites/tileset/world_objects/bush_16x16.png').convert_alpha(), # 7
    'bush_eaten': pg.image.load('assets/sprites/tileset/world_objects/bush_eaten_16x16.png').convert_alpha(), # 12
    'spawn_point_off': pg.image.load('assets/sprites/tileset/world_objects/spawnpoint_off.png').convert_alpha(), # 13
    'spawn_point_on': pg.image.load('assets/sprites/tileset/world_objects/spawnpoint_on.png').convert_alpha(), # 14
    'box': pg.image.load('assets/sprites/box.png').convert_alpha(),

                 }
