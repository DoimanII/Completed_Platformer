import time

import pygame as pg
pg.init()

keys = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, 'F3':False}

WIN_SIZE = (1280, 720)
SCALE = 4
screen = pg.display.set_mode(WIN_SIZE, vsync=1) # , pg.FULLSCREEN
WIN_RES = (screen.get_size()[0] // SCALE, screen.get_size()[1] // SCALE)
display = pg.Surface(WIN_RES)


clock = pg.time.Clock()
FPS = 60

timer = 0

animation_database = {}
animation_higher_database = {}

TILE_SIZE = 16

tile_database = {
    'grass':pg.image.load('assets/sprites/tileset/ground_tiles/grass_16x16.png').convert_alpha(), # TileSet 0
    'grass32x16':pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x16.png').convert_alpha(), # 1
    'grass32x32':pg.image.load('assets/sprites/tileset/ground_tiles/grass_32x32.png').convert_alpha(), # 2
    'grass128x128':pg.image.load('assets/sprites/tileset/ground_tiles/BIG_grass_128x128.png').convert_alpha(), # 9


    'dirt':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_16x16.png').convert_alpha(), # 3
    'dirt32x16':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x16.png').convert_alpha(), # 4
    'dirt32x32':pg.image.load('assets/sprites/tileset/ground_tiles/dirt_32x32.png').convert_alpha(), # 5
    'dirt128x128':pg.image.load('assets/sprites/tileset/ground_tiles/BIG_dirt_128x128.png').convert_alpha(), # 10

    'left_grassramp_16x16':pg.image.load('assets/sprites/tileset/ground_tiles/left_grassramp_16x16.png').convert_alpha(),
    'right_grassramp_16x16':pg.image.load('assets/sprites/tileset/ground_tiles/right_grassramp_16x16.png').convert_alpha(),

    'right_littlegrass_16x16':pg.image.load('assets/sprites/tileset/ground_tiles/right_littlegrass_16x16.png').convert_alpha(),
    'left_littlegrass_16x16':pg.image.load('assets/sprites/tileset/ground_tiles/left_littlegrass_16x16.png').convert_alpha(),

    'little_tree':pg.image.load('assets/sprites/tileset/world_objects/little_tree_16x16.png').convert_alpha(), # World Obj 6
    'plant':pg.image.load('assets/sprites/tileset/world_objects/plant_16x16.png').convert_alpha(), # 8
    'tree_01':pg.image.load('assets/sprites/tileset/world_objects/tree_01_64x80.png').convert_alpha(),
    'tree_02':pg.image.load('assets/sprites/tileset/world_objects/tree_02_80x96.png').convert_alpha(),
    'tree_03': pg.image.load('assets/sprites/tileset/world_objects/tree_03_48_64.png').convert_alpha(),

    'spikes': pg.image.load('assets/sprites/spikes.png').convert_alpha(), # Entity sprites 11
    'bush': pg.image.load('assets/sprites/tileset/world_objects/bush_16x16.png').convert_alpha(), # 7
    'bush_eaten': pg.image.load('assets/sprites/tileset/world_objects/bush_eaten_16x16.png').convert_alpha(), # 12
    'spawn_point_off': pg.image.load('assets/sprites/tileset/world_objects/spawnpoint_off.png').convert_alpha(), # 13
    'spawn_point_on': pg.image.load('assets/sprites/tileset/world_objects/spawnpoint_on.png').convert_alpha(), # 14
    'box': pg.image.load('assets/sprites/box.png').convert_alpha(),

    #BG tiles
    'bg_dirt':pg.image.load('assets/sprites/tileset/back_ground_tiles/dirt_16x16.png').convert_alpha(),
    'bg_dirt_3x3':pg.image.load('assets/sprites/tileset/back_ground_tiles/dirt_48x48.png').convert_alpha(),
    'bg_grass':pg.image.load('assets/sprites/tileset/back_ground_tiles/grass_16x16.png').convert_alpha(),
    'bg_grass_3x3':pg.image.load('assets/sprites/tileset/back_ground_tiles/grass_48x48.png').convert_alpha(),
    'bg_left_ramp':pg.image.load('assets/sprites/tileset/back_ground_tiles/left_ramp_16x32.png').convert_alpha(),
    'bg_right_ramp':pg.image.load('assets/sprites/tileset/back_ground_tiles/right_ramp_16x32.png').convert_alpha(),

    # GUI
    'MenuBG': pg.image.load('assets/levels/maps/MenuBG.png').convert_alpha(),
    'BlueButtonUp': pg.image.load('assets/sprites/GUI/BlueButtonUp.png').convert_alpha(),
    'BlueButtonDown': pg.image.load('assets/sprites/GUI/BlueButtonDown.png').convert_alpha(),
                 }

sounds_database = {'bg_sounds': [pg.mixer.music.load('assets/sounds/bg_sound.mp3')],
    'player':{'walk':[[pg.mixer.Sound(f'assets/sounds/player/walk/step_{i}.mp3') for i in range(2)], 0],
                             'jump':[[pg.mixer.Sound('assets/sounds/player/jump/jump_0.mp3')], 0],
                             'hit':[[pg.mixer.Sound(f'assets/sounds/player/hit/hit-{i}-3.mp3') for i in range(3)], 0]}}


for sound in sounds_database['player']['walk'][0]:
    sound.set_volume(0.1)
for sound in sounds_database['player']['hit'][0]:
    sound.set_volume(0.2)
for sound in sounds_database['player']['jump'][0]:
    sound.set_volume(0.1)
BACKGROUND_COLOR = (134, 212, 229)
