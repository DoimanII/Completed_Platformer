import pygame as pg

M = 4


FPS = 60


keys = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, }
WIN_SIZE = (1280, 720)
screen = pg.display.set_mode(WIN_SIZE) # , pg.FULLSCREEN

WIN_RES = (screen.get_size()[0]//M, screen.get_size()[1]//M)
display = pg.Surface(WIN_RES)
clock = pg.time.Clock()

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
    7:pg.image.load('assets/sprites/tileset/world_objects/bush_16x16.png').convert_alpha(),
    8:pg.image.load('assets/sprites/tileset/world_objects/plant_16x16.png').convert_alpha()
                 }