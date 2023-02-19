import pygame as pg
from Settings import *


def load_animation(path):
    global animation_higher_database, animation_database
    with open(path + 'entity_animation.txt', 'r') as file:
        data = file.read()
    for animation in data.split('\n'):
        section = animation.split(' ')
        animation_info = section[0].split('/')
        img_scale = int(section[2])

        entity_name = animation_info[1]
        animation_name = animation_info[-1]
        if entity_name not in animation_higher_database:
            animation_higher_database[entity_name] = {}
        if animation_name not in animation_higher_database[entity_name]:
            animation_higher_database[entity_name][animation_name] = []

        frame_duration = section[1].split(';')
        n = 0
        for frame in frame_duration:
            animation_path = path + section[0] + '/' + animation_name + '_' + str(n) + '.png'
            image = pg.image.load(animation_path).convert_alpha()
            image = pg.transform.scale(image, (image.get_size()[0] * img_scale, image.get_size()[1] * img_scale))
            animation_database[animation_path] = image

            for i in range(int(frame)):
                animation_higher_database[entity_name][animation_name].append(animation_path)
            n += 1

def load_level_from_image(image):
    tile_map = []
    entity_map = []
    world_obj_map = []

    rsize = 16
    sprites_dict = {
        (115, 100, 100, 255): (115, 100, 100, 255),
        (0, 0, 0, 0): (0, 0, 0, 0),

        (126,202,74, 255): (0, (rsize, rsize), 'tile'),
        (111, 194, 54, 255): (1, (rsize*2, rsize), 'tile'),
        (81, 177, 16, 255): (2, (rsize * 2, rsize*2), 'tile'),
        (50, 123, 0, 255): (9, (rsize * 8, rsize * 8), 'tile'),

        (134, 74, 46, 255): (3, (rsize, rsize), 'tile'),
        (70, 32, 13, 255): (10, (rsize*8, rsize*8), 'tile'),

        (16, 200, 64, 255): (8, (rsize, rsize), 'wob'),
        (3, 148, 41, 255): (7, (rsize, rsize), 'wob'),
        (0, 82, 21, 255): (6, (rsize, rsize), 'wob'),

                    }
    width = image.get_width()
    height = image.get_height()

    for y in range(0, height):
        for x in range(0, width):
            color_got = tuple(image.get_at((x, y)))
            if color_got != sprites_dict[(115, 100, 100, 255)] and color_got != sprites_dict[(0, 0, 0, 0)]:
                inx, size = sprites_dict[color_got][0], sprites_dict[color_got][1]
                pos = x*rsize, y*rsize
                rect = pg.Rect(pos, size)

                if sprites_dict[color_got][2] == 'tile':
                    tile_map.append([inx, rect])
                if sprites_dict[color_got][2] == 'entity':
                    entity_map.append([inx, rect])
                if sprites_dict[color_got][2] == 'wob':
                    world_obj_map.append([inx, rect])

    return tile_map, world_obj_map, entity_map

def get_mouse_pos():
    position = pg.mouse.get_pos()
    position = position[0] // M, position[1] // M
    return position

def simple_camera(rect, display):
    return int(rect.x - display.get_width() / 2 + rect.width / 2), int(
        rect.y - display.get_height() / 2 + rect.height / 2)


class GUI():
    def __init__(self):
        self.sprites = []
        self.font = pg.font.Font(None, 8)

    def entity_HP(self, rect, camera, hp):
        hp_rect = pg.Rect(rect.x-camera[0]+1, rect.y-camera[1]-4, int(0.14*hp), 1)
        pg.draw.rect(display, 'red', hp_rect)


class Physics():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def __test_collide(self, tiles=None, entities=None):
        hit_list = []

        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile[1]):
                    dict = {'rect': tile[1], 'name': tile[0]}
                    hit_list.append(dict)
        if entities:
            for entity in entities:
                if self.rect.colliderect(entity.obj.rect):
                    dict = {'rect': entity.obj.rect, 'name': entity.name}
                    hit_list.append(dict)
        return hit_list

    def move(self, movement, tiles=None, entities=None):
        collision_type = {'top': False, 'bottom': False, 'left': False, 'right': False}
        tile_name = None
        # X-axis
        self.rect.x += int(movement[0])
        hit_list = self.__test_collide(tiles, entities)
        for hit in hit_list:
            if movement[0] > 0:
                self.rect.right = hit['rect'].left
                collision_type['right'] = True
                tile_name = hit['name']
            if movement[0] < 0:
                self.rect.left = hit['rect'].right
                collision_type['left'] = True
                tile_name = hit['name']

        # Y-axis
        self.rect.y += int(movement[1])
        hit_list = self.__test_collide(tiles, entities)
        for hit in hit_list:
            if movement[1] > 0:
                self.rect.bottom = hit['rect'].top
                collision_type['bottom'] = True
                tile_name = hit['name']
            if movement[1] < 0:
                self.rect.top = hit['rect'].bottom
                collision_type['top'] = True
                tile_name = hit['name']
        return {'collision':collision_type, 'name':tile_name}


class Entity():
    def __init__(self, name, x, y, width, height, image=None):
        self.name = name
        self.obj = Physics(x, y, width, height)

        self.image = image
        self.animation = None if name not in animation_higher_database else animation_higher_database[name]
        self.animation_speed = 1
        self.frame = 0

        self.alpha = 255
        self.rotation = 0
        self.flip_x, self.flip_y = False, False
        self.action = 'idle'

    def get_rect(self):
        return self.obj.rect

    def get_size(self):
        return self.obj.rect.size

    def get_pos(self):
        return self.obj.rect.topleft

    def set_pos(self, pos):
        self.obj.rect.topleft = pos

    def set_size(self, size):
        self.obj.rect.size = size

    def move(self, movement, tiles=None, entities=None):
        return self.obj.move(movement, tiles, entities)

    def collide_point(self, point):
        return self.obj.rect.collidepoint(point)

    def collide_rect(self, rect):
        return self.obj.rect.colliderect(rect)

    def flip(self, image):
        return pg.transform.flip(image, self.flip_x, self.flip_y)

    def render(self, display, dt, camera=(0, 0)):
        image_to_render = None
        if self.image != None:
            image_to_render = self.flip(self.image)

        if self.image == None:
            self.frame += self.animation_speed * dt
            if self.frame >= len(self.animation[self.action]):
                self.frame = 0
            img_id = self.animation[self.action][int(self.frame)]
            image_to_render = self.flip(animation_database[img_id])

        if image_to_render != None:
            self.set_size(image_to_render.get_size())
            image_to_render.set_alpha(self.alpha)
            image_to_render = pg.transform.rotate(image_to_render, self.rotation)

            pos = self.get_pos()[0] - camera[0], self.get_pos()[1] - camera[1]
            display.blit(image_to_render, pos)
