import pygame as pg
import random
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
    background = []
    player = None

    rsize = 16
    sprites_dict = {
        (115, 100, 100, 255): (115, 100, 100, 255),
        (0, 0, 0, 0): (0, 0, 0, 0),
        (151, 155, 156, 255): (151, 155, 156, 255),

        (126, 202, 74, 255): (0, (rsize, rsize), 'tile'),
        (111, 194, 54, 255): (1, (rsize * 2, rsize), 'tile'),
        (81, 177, 16, 255): (2, (rsize * 2, rsize * 2), 'tile'),
        (50, 123, 0, 255): (9, (rsize * 8, rsize * 8), 'tile'),

        (134, 74, 46, 255): (3, (rsize, rsize), 'tile'),
        (121, 67, 42, 255): (4, (rsize * 2, rsize), 'tile'),
        (121, 55, 24, 255): (5, (rsize * 2, rsize * 2), 'tile'),
        (70, 32, 13, 255): (10, (rsize * 8, rsize * 8), 'tile'),

        (16, 200, 64, 255): (8, (rsize, rsize), 'wob'),
        (3, 148, 41, 255): (6, (rsize, rsize), 'wob'),
        (55, 148, 110, 255): (0.25, (rsize * 4, rsize * 15), 'bg'),
        (63, 181, 133, 255): (0.5, (rsize * 3, rsize * 15), 'bg'),

        (255, 255, 255, 255): (Entity('entity_test', 0, 0, 0, 0), (0, 0), 'player'),
        (121, 46, 106, 255): ('spikes', (0, 0), 'entity'),
        (0, 82, 21, 255): ('bush', (16, 16), 'entity'),
    }
    width = image.get_width()
    height = image.get_height()

    for y in range(0, height):
        for x in range(0, width):
            color_got = tuple(image.get_at((x, y)))
            if color_got != sprites_dict[(115, 100, 100, 255)] and color_got != sprites_dict[
                (0, 0, 0, 0)] and color_got != sprites_dict[(151, 155, 156, 255)]:
                inx, size = sprites_dict[color_got][0], sprites_dict[color_got][1]
                pos = [x * rsize, y * rsize]
                rect = pg.Rect(pos, size)

                if sprites_dict[color_got][2] == 'tile':
                    tile_map.append([inx, rect])
                if sprites_dict[color_got][2] == 'player':
                    player = inx
                    player.set_pos(pos)
                if sprites_dict[color_got][2] == 'wob':
                    world_obj_map.append([inx, rect])
                if sprites_dict[color_got][2] == 'bg':
                    rect.topleft = x*rsize-rsize*4, y*rsize-rsize*6
                    background.append([rect, inx, color_got])

                if sprites_dict[color_got][2] == 'entity':
                    if inx == 'spikes':
                        size = rsize, rsize - 5
                        pos[1] += 5
                        entity = Entity(inx, *pos, *size, tile_database[11])
                        entity.id = len(entity_map)
                        entity_map.append(entity)
                    if inx == 'bush':
                        size = rsize, rsize - 5
                        entity = Entity(inx, *pos, *size, tile_database[7])
                        entity.iscollision = False
                        entity.id = len(entity_map)
                        entity_map.append(entity)

    return tile_map, world_obj_map, entity_map, background, player

def get_mouse_pos():
    position = pg.mouse.get_pos()
    position = position[0] // SCALE, position[1] // SCALE
    return position


class User():
    def simple_player_animation(self, movement, entity):
        if movement[0] == 0:
            entity.action = 'idle'
            entity.animation_speed = 1
        if movement[0] != 0:
            entity.action = 'walk'
            entity.animation_speed = 6

    def health(self, entity, check_point):
        if entity.HP > 100:  # Работаем со здоровьем
            entity.HP = 100
        if entity.HP < 0:
            entity.HP = 0
            self.death(entity, check_point)

    def death(self, entity, check_point):
        if entity.HP <= 0:
            entity.set_pos(check_point)
            entity.HP = 100
    def simple_camera(self, rect, display):
        return int(rect.x - display.get_width() / 2 + rect.width / 2), int(
            rect.y - display.get_height() / 2 + rect.height / 2)

    def user_input(self, entity, tiles, entities, dt, check_point):
        movement = [0, 0]
        entity.y_momentum += 20 * dt  # Падаем

        if keys['right']:  # key input
            movement[0] = round(entity.speed * dt)
            entity.flip_x = True
        if keys['left']:
            movement[0] = round(-entity.speed * dt)
            entity.flip_x = False
        if keys['up'] and entity.collision['collision']['bottom']:
            if entity.air_timer < 10:
                entity.y_momentum = - entity.jump_height * dt
        # Ограничиваем скорость падения и прыжка
        if entity.y_momentum > 3:  # Максимальная скорость падения
            entity.y_momentum = 3
        if entity.y_momentum < -6:  # Максимальная скорость прыжка
            entity.y_momentum = -6
        movement[1] = round(entity.y_momentum)

        entity.collision = entity.move(movement, tiles, entities)  # collision
        if entity.collision['collision']['bottom'] or entity.collision['collision'][
            'top']:  # Если мы стоим на земле или прыгнули до потолка
            entity.y_momentum = 1
            if entity.air_timer > 1:
                entity.HP -= 10 + int(entity.air_timer * 20)
            entity.air_timer = 0
        else:
            entity.air_timer += 1 * dt

        self.simple_player_animation(movement, entity)  # Анимируем
        self.health(entity, check_point)


        return movement

class EntityAssets():
    def spikes(self, entity, player, dt):
        if entity.name == player.collision['name'][0]:
            if entity.name == 'spikes' and player.collision['collision']['bottom'] and entity.id == \
                    player.collision['name'][1]:
                player.y_momentum -= 450 * dt
                player.HP -= 10
    def bush(self, entity, player, dt):
        if player.collide_rect(entity.get_rect()) and entity.name == 'bush' and keys[
            'action'] and not entity.used and player.HP < 100:
            entity.used = True
            entity.image = tile_database[12]
            player.HP += random.choice([20, 30, 40, 50])


    def spawn_point_entity(self, entity, player, check_point): # WORKING IN PROGRESS!
        if entity.name == 'spawn' and player.collide_rect(entity.get_rect()):
            if keys['action'] and not entity.used:
                entity.used = True
                entity.image = tile_database[14]
                return entity.get_pos
            else:
                return check_point



    # Неплохо! Но надо думать дальше. Еще нашлась проблема с коллизиями. Мы запоминаем лишь один объект, с которым сталкиваемся, хотя по факту мы можем столкнуться с кучей объектов
    def test(self, entity, player, pl_movement, tiles, dt):
        if entity.name == 'test':
            movement = [0, 0]
            if player.collision['name'][0] == 'test' and (
                    player.collision['collision']['left'] or player.collision['collision']['right']):
                movement[0] = pl_movement[0]
            entity.y_momentum += 20 * dt  # Падаем

            if entity.y_momentum > 3:  # Максимальная скорость падения
                entity.y_momentum = 3
            if entity.y_momentum < -6:  # Максимальная скорость прыжка
                entity.y_momentum = -6
            movement[1] = round(entity.y_momentum)
            entity.collision = entity.move(movement, tiles)
            if entity.collision['collision']['bottom'] or entity.collision['collision'][
                'top']:  # Если мы стоим на земле или прыгнули до потолка
                entity.y_momentum = 1
                if entity.air_timer > 1:
                    entity.HP -= 10 + int(entity.air_timer * 20)
                entity.air_timer = 0
            else:
                entity.air_timer += 1 * dt





class GUI():
    def __init__(self):
        self.sprites = []
        self.font = pg.font.Font(None, 32)

    def entity_HP(self, rect, camera, hp):
        hp_rect = pg.Rect(rect.x - camera[0] + 1, rect.y - camera[1] - 4, int(0.14 * hp), 1)
        pg.draw.rect(display, 'red', hp_rect)

    def message(self, data_dict):
        for tag in data_dict:
            text, pos, color, font, show = data_dict[tag]['text'], data_dict[tag]['pos'], data_dict[tag]['color'], data_dict[tag]['font'], data_dict[tag]['show']
            if show:
                surf = font.render(str(text), False, color)
                rect = surf.get_rect(topleft=pos)
                screen.blit(surf, rect)

class Physics():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def __test_collide(self, tiles=None, entities=None):
        hit_list = []

        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile[1]):
                    dict = {'rect': tile[1], 'name': ('tile', tile[0])}
                    hit_list.append(dict)
        if entities:
            for entity in entities:
                if self.rect.colliderect(entity.obj.rect) and entity.iscollision:
                    dict = {'rect': entity.obj.rect, 'name': (entity.name, entity.id), }
                    hit_list.append(dict)
        return hit_list

    def move(self, movement, tiles=None, entities=None):
        collision_type = {'top': False, 'bottom': False, 'left': False, 'right': False}
        tile_name = [None, None]
        # X-axis
        self.rect.x += int(movement[0])
        hit_list = self.__test_collide(tiles, entities)
        for hit in hit_list:
            if movement[0] > 0:
                self.rect.right = hit['rect'].left
                collision_type['right'] = True
                tile_name = (hit['name'])
            if movement[0] < 0:
                self.rect.left = hit['rect'].right
                collision_type['left'] = True
                tile_name = (hit['name'])

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
        return {'collision': collision_type, 'name': tile_name}


class Entity():
    def __init__(self, name, x, y, width, height, image=None, iscollision = True):
        self.name = name
        self.id = 0
        self.obj = Physics(x, y, width, height)
        self.collision = {'collision': {'top': False, 'bottom': False, 'left': False, 'right': False},
                          'name': [None, None]}
        self.iscollision = iscollision

        self.image = image
        self.animation = None if name not in animation_higher_database else animation_higher_database[name]
        self.animation_speed = 1
        self.frame = 0

        self.alpha = 255
        self.rotation = 0
        self.flip_x, self.flip_y = False, False
        self.action = 'idle'

        self.HP = 100
        self.air_timer = 0
        self.y_momentum = 0
        self.speed = 200
        self.jump_height = 300
        self.used = False

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
