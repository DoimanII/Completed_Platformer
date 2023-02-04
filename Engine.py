import pygame as pg
from Settings import *


def load_animation(path):
    global animation_higher_database
    with open(path + 'entity_animation.txt', 'r') as f:
        data = f.read()
    for animation in data.split('\n'):
        sections = animation.split(' ')

        animation_info = sections[0].split('/')
        entity_name = animation_info[1]
        animation_name = animation_info[-1]
        if entity_name not in animation_higher_database:
            animation_higher_database[entity_name] = {}
        if animation_name not in animation_higher_database[entity_name]:
            animation_higher_database[entity_name][animation_name] = []
        frame_duration = sections[1].split(';')
        n = 0
        for frame in frame_duration:
            animation_path = path + sections[0] + '/' + animation_name + '_' + str(n) + '.png'
            animation_database[animation_path] = pg.transform.scale2x(pg.image.load(animation_path)).convert_alpha()
            for i in range(int(frame)):
                animation_higher_database[entity_name][animation_name].append(animation_path)
            n += 1


def get_mouse_pos():
    position = pg.mouse.get_pos()
    position = position[0] // M, position[1] // M
    return position


class Physics():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def __test_collide(self, tiles=None, entities=None):
        hit_list = []
        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile):
                    dict = {'rect': tile, 'name': 'tile'}
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
        return collision_type, tile_name


class Entity():
    def __init__(self, x, y, width, height, image=None):
        self.obj = Physics(x, y, width, height)

        self.image = image
        self.frame = 0

        self.alpha = 0
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
        self.obj.move(movement, tiles, entities)

    def collide_point(self, point):
        return self.obj.rect.collidepoint(point)

    def collide_rect(self, rect):
        return self.obj.rect.colliderect(rect)

    def flip(self, image):
        return pg.transform.flip(image, self.flip_x, self.flip_y)
'''
class Entity():
    def __init__(self, name, x, y, width, height, image=None, id=42):
        self.name = name
        self.id = id

        self.obj = physics(x, y, width, height)

        self.image = image
        self.frame = 0
        self.color = (0, 0, 0)

        self.alpha = None
        self.rotation = 0
        self.flip_x = False
        self.flip_y = False
        self.action = 'idle'

    def get_pos(self):
        return (self.obj.rect.x, self.obj.rect.y)

    def get_size(self):
        return (self.obj.rect.width, self.obj.rect.height)

    def get_rect(self):
        return self.obj.rect

    def set_pos(self, x, y):
        self.obj.rect.x = x
        self.obj.rect.y = y

    def set_size(self, width, height):
        self.obj.rect.width = width
        self.obj.rect.height = height

    # def move(self, movement, tiles):
    #    self.obj.move(movement, tiles)

    def collide_rect(self, rect):
        if self.obj.rect.colliderect(rect):
            return True

    def collide_point(self, point):
        if self.obj.rect.collidepoint(point):
            return True

    def flip(self, img):
        return pg.transform.flip(img, self.flip_x, self.flip_y)

    def render(self, display, camera=(0, 0)):
        image_to_render = None
        if self.image != None:
            image_to_render = self.image
            self.set_size(*image_to_render.get_size())

        if self.name in animation_higher_database and self.action in animation_higher_database[self.name]:
            self.frame += 1
            if self.frame > len(animation_higher_database[self.name][self.action]) - 1:
                self.frame = 0
            img_id = animation_higher_database[self.name][self.action][self.frame]
            image_to_render = animation_database[img_id]
            self.set_size(*image_to_render.get_size())

        if image_to_render != None:
            image_to_render = pg.transform.rotate(image_to_render, self.rotation)
            display.blit(self.flip(image_to_render), (self.get_pos()[0] - camera[0], self.get_pos()[1] - camera[1]))

        else:
            pg.draw.rect(display, self.color,
                         (self.get_pos()[0] - camera[0], self.get_pos()[1] - camera[1], *self.get_size()))
'''
