import pygame as pg
import random
from Settings import *


def color_swap(img, old_c, new_c):
    surf_w, surf_h = img.get_size()
    if len(old_c) != len(new_c):
        return img

    for i in range(len(old_c)):
        for x in range(surf_w):
            for y in range(surf_h):
                if img.get_at((x, y)) == old_c[i]:
                    img.set_at((x, y), new_c[i])
    return img


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
    triggers = []
    player = None

    rsize = 16
    sprites_dict = {
        (115, 100, 100, 255): (115, 100, 100, 255),
        (0, 0, 0, 0): (0, 0, 0, 0),
        (151, 155, 156, 255): (151, 155, 156, 255),

        (104, 255, 0, 255): ('left_grassramp_16x16', (rsize, rsize), 'ramp', 1),
        (144, 251, 70, 255): ('right_grassramp_16x16', (rsize, rsize), 'ramp', 2),

        (29, 66, 3, 255): ('left_littlegrass_16x16', (rsize, rsize), 'tile'),
        (17, 41, 1, 255): ('right_littlegrass_16x16', (rsize, rsize), 'tile'),

        (126, 202, 74, 255): ('grass', (rsize, rsize), 'tile'),
        (111, 194, 54, 255): ('grass32x16', (rsize * 2, rsize), 'tile'),
        (81, 177, 16, 255): ('grass32x32', (rsize * 2, rsize * 2), 'tile'),
        (50, 123, 0, 255): ('grass128x128', (rsize * 8, rsize * 8), 'tile'),

        (134, 74, 46, 255): ('dirt', (rsize, rsize), 'tile'),
        (121, 67, 42, 255): ('dirt32x16', (rsize * 2, rsize), 'tile'),
        (121, 55, 24, 255): ('dirt32x32', (rsize * 2, rsize * 2), 'tile'),
        (70, 32, 13, 255): ('dirt128x128', (rsize * 8, rsize * 8), 'tile'),

        (16, 200, 64, 255): ('plant', (rsize, rsize), 'wob'),
        (3, 148, 41, 255): ('little_tree', (rsize, rsize), 'wob'),
        (107, 56, 32, 255): ('tree_01', (rsize * 4, rsize * 8), 'wob'),
        (123, 79, 58, 255): ('tree_02', (rsize * 8, rsize * 9), 'wob'),
        (123, 91, 76, 255): ('tree_03', (rsize * 4, rsize * 3), 'wob'),

        (55, 148, 110, 255): (0.25, (rsize * 4, rsize * 39), 'bg'),
        (63, 181, 133, 255): (0.35, (rsize * 3, rsize * 39), 'bg'),

        (134, 74, 46, 100): ('bg_dirt', (rsize, rsize), 'bg'),
        (121, 55, 24, 100): ('bg_dirt_3x3', (rsize*3, rsize*3), 'bg'),
        (126, 202, 74, 100): ('bg_grass', (rsize, rsize), 'bg'),
        (81, 177, 16, 100): ('bg_grass_3x3', (rsize*3, rsize*3), 'bg'),
        (104, 255, 0, 100): ('bg_left_ramp', (rsize, rsize), 'bg'),
        (144, 251, 70, 100): ('bg_right_ramp', (rsize, rsize), 'bg'),


        (255, 255, 255, 255): (Entity('entity_test', 0, 0, 0, 0), (0, 0), 'player'),

        (121, 46, 106, 255): ('spikes', (0, 0), 'entity'),
        (0, 82, 21, 255): ('bush', (16, 16), 'entity'),
        (100, 160, 59, 255): ('fblock', (16, 16), 'entity'),
        (194, 80, 23, 255): ('pblock', (16, 16), 'entity'),

        (255, 0, 0, 255): ('spawn', (16, 16), 'entity'),
        (0, 0, 255, 255): ('blue', (16, 16), 'trigger'),
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
                if sprites_dict[color_got][2] == 'ramp':  # ['left_grassramp_16x16', pg.Rect(320, 736+16, 16, 16), 1]
                    ramp_type = sprites_dict[color_got][3]
                    tile_map.append([inx, rect, ramp_type])
                if sprites_dict[color_got][2] == 'player':
                    player = inx
                    player.set_pos(pos)
                if sprites_dict[color_got][2] == 'wob':
                    world_obj_map.append([inx, rect])
                if sprites_dict[color_got][2] == 'bg':
                    if type(inx) == float:
                        rect.topleft = x * rsize - rsize * 4, y * 6
                        background.append([rect, inx, color_got])
                    else:

                        background.append([rect, inx, color_got])

                if sprites_dict[color_got][2] == 'trigger':
                    if inx == 'blue':
                        triggers.append(Trigger(pos, size, len(triggers)))

                if sprites_dict[color_got][2] == 'entity':
                    if inx == 'spawn':
                        size = rsize, rsize - 5

                        entity = Entity(inx, *pos, *size, tile_database['spawn_point_off'], False, )
                        entity.id = len(entity_map)
                        entity_map.append(entity)

                    if inx == 'spikes':
                        size = rsize, rsize - 5
                        pos[1] += 5
                        entity = Entity(inx, *pos, *size, tile_database['spikes'])
                        entity.id = len(entity_map)
                        entity_map.append(entity)

                    if inx == 'bush':
                        size = rsize, rsize - 5
                        entity = Entity(inx, *pos, *size, tile_database['bush'])
                        entity.iscollision = False
                        entity.id = len(entity_map)
                        entity_map.append(entity)

                    if inx == 'fblock':
                        size = rsize, rsize - 5
                        entity = Entity(inx, *pos, *size, tile_database['grass'])
                        entity.id = len(entity_map)
                        entity_map.append(entity)

                    if inx == 'pblock':
                        size = rsize, rsize - 5
                        entity = Entity(inx, *pos, *size, tile_database['box'])
                        entity.id = len(entity_map)
                        entity_map.append(entity)

    return tile_map, world_obj_map, entity_map, background, player, triggers


def get_mouse_pos():
    position = pg.mouse.get_pos()
    position = position[0] // SCALE, position[1] // SCALE
    return position


class User():
    def __init__(self, camera_boarders={'left': 105, 'right': 105, 'top': 30, 'bottom': 30}):
        # box setup
        self.screen_shake_timer = 0
        self.keyboarder_speed = 5
        self.mouse_speed = 5
        self.camera_boarders = camera_boarders
        self.camera_rect = pg.Rect(self.camera_boarders['left'], self.camera_boarders['top'],
                                   display.get_width() - (self.camera_boarders['left'] + self.camera_boarders['right']),
                                   display.get_height() - (
                                           self.camera_boarders['top'] + self.camera_boarders['bottom']))

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
            self.screen_shake_timer = 5
            entity.set_pos(check_point)
            entity.HP = 100

    def simple_camera(self, rect, display):
        return int(rect.centerx - display.get_width() / 2), int(rect.centery - display.get_height() / 2)

    def box_target_camera(self, target):
        if target.left < self.camera_rect.left:
            self.camera_rect.left = target.left
        if target.right > self.camera_rect.right:
            self.camera_rect.right = target.right

        if target.top < self.camera_rect.top:
            self.camera_rect.top = target.top
        if target.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.bottom

        return self.camera_rect.left - self.camera_boarders['left'], self.camera_rect.top - self.camera_boarders['top']

    def mouse_control_camera(self, dt=1):
        m_pos = pg.math.Vector2(pg.mouse.get_pos()[0] // SCALE, pg.mouse.get_pos()[1] // SCALE)
        if m_pos.x <= self.camera_boarders['left']:
            self.camera_rect.centerx -= self.mouse_speed * dt
        if m_pos.x >= WIN_RES[0] - self.camera_boarders['right']:
            self.camera_rect.centerx += self.mouse_speed * dt

        if m_pos.y <= self.camera_boarders['top']:
            self.camera_rect.centery -= self.mouse_speed * dt
        if m_pos.y >= WIN_RES[1] - self.camera_boarders['bottom']:
            self.camera_rect.centery += self.mouse_speed * dt

        return self.camera_rect.left - self.camera_boarders['left'], self.camera_rect.top - self.camera_boarders['top']

    def user_input(self, entity, tiles, entities, dt, check_point):
        movement = pg.math.Vector2()
        entity.y_momentum += 20 * dt  # Падаем
        if sounds_database['player']['walk'][1] > 0:
            sounds_database['player']['walk'][1] -= 1
        if keys['right']:  # key input
            movement[0] = round(entity.speed * dt)
            entity.flip_x = True

            # particles creation
            vel = pg.math.Vector2(-300, random.randint(-100, 100))
            pos = pg.math.Vector2(*entity.get_rect().midbottom)
            color = 'white'
            pos.y -= 2
            entity.particles.append([pos, vel, random.randint(3, 5), color]) if entity.collision['bottom'][
                'collided'] else None
        if keys['left']:
            movement[0] = round(-entity.speed * dt)
            entity.flip_x = False

            # particles creation
            vel = pg.math.Vector2(300, random.randint(-100, 100))
            pos = pg.math.Vector2(*entity.get_rect().midbottom)
            color = 'white'
            pos.y -= 2
            entity.particles.append([pos, vel, random.randint(3, 5), color]) if entity.collision['bottom'][
                'collided'] else None
        if keys['up'] and entity.collision['bottom']['collided']:
            sounds_database['player']['jump'][0][0].play()
            if entity.air_timer < 10:
                entity.y_momentum = - entity.jump_height * dt
        # Ограничиваем скорость падения и прыжка
        if entity.y_momentum > 3:  # Максимальная скорость падения
            entity.y_momentum = 3
        if entity.y_momentum < -6:  # Максимальная скорость прыжка
            entity.y_momentum = -6
        movement[1] = round(entity.y_momentum)

        entity.collision = entity.move(movement, tiles, entities)  # collision
        if entity.collision['bottom']['collided'] or entity.collision['top'][
            'collided']:  # Если мы стоим на земле или прыгнули до потолка
            entity.y_momentum = 1
            if entity.air_timer > 1:
                entity.screen_shake_timer = 10
                for i in range(20):
                    entity.particles.append([pg.math.Vector2(*entity.get_rect().center),
                                             pg.math.Vector2(random.randint(-200, 200), random.randint(-1, 1)),
                                             random.randint(2, 5), 'red'])

                entity.HP -= 10 + int(entity.air_timer * 20)
                sounds_database['player']['hit'][0][random.randint(0, 2)].play()
            entity.air_timer = 0
        else:
            entity.air_timer += 1 * dt
        # Sound play
        if entity.collision['bottom']['collided'] and movement.x != 0 and sounds_database['player']['walk'][1] == 0:
            sounds_database['player']['walk'][1] = 20
            sounds_database['player']['walk'][0][random.randint(0, 1)].play()

        self.simple_player_animation(movement, entity)  # Анимируем
        self.health(entity, check_point)

        return movement


class EntityAssets():
    def spikes(self, entity, player, dt):
        if entity.name == (
                player.collision['top']['name'] or player.collision['bottom']['name'] or player.collision['left'][
            'name'] or player.collision['right']['name']):
            if entity.name == 'spikes' and player.collision['bottom']['collided'] and entity.id == \
                    player.collision['bottom']['id']:
                player.y_momentum -= 450 * dt
                player.HP -= 35
                sounds_database['player']['hit'][0][random.randint(0, 2)].play()

                player.screen_shake_timer = 10
                for i in range(20):
                    player.particles.append([pg.math.Vector2(*player.get_rect().center),
                                             pg.math.Vector2(random.randint(-200, 200), random.randint(-100, 100)),
                                             random.randint(3, 8), 'red'])

    def bush(self, entity, player, dt):
        if player.collide_rect(entity.get_rect()) and entity.name == 'bush' and keys[
            'action'] and not entity.used and player.HP < 100:
            entity.used = True
            entity.image = tile_database['bush_eaten']
            player.HP += random.choice([20, 30, 40, 50])

    def spawn_point_entity(self, entity, player, check_point):  # WORKING IN PROGRESS!
        if entity.name == 'spawn' and player.collide_rect(entity.get_rect()):
            if not entity.used:
                for i in range(20):
                    entity.particles.append([pg.math.Vector2(*entity.get_rect().center),
                                             pg.math.Vector2(random.randint(-100, 100), random.randint(-100, 100)),
                                             random.randint(15, 25), (
                                             random.randint(100, 255), random.randint(100, 255),
                                             random.randint(100, 255))])

                entity.used = True
                entity.image = tile_database['spawn_point_on']
                return True

    def falling_block(self, entity, player, tiles, enitiies, dt):
        if entity.name == 'fblock':
            movement = [0, 0]
            if player.collision['bottom']['name'] == entity.name and player.collision['bottom']['id'] == entity.id:
                entity.used = True
            if entity.collision['bottom']['name'] == 'spikes':
                enitiies.remove(entity)
            if entity.used:
                entity.y_momentum += 20 * dt
                if entity.y_momentum > 3:  # Максимальная скорость падения
                    entity.y_momentum = 3
                if entity.y_momentum < -6:  # Максимальная скорость прыжка
                    entity.y_momentum = -6
                movement[1] = round(entity.y_momentum)
                entity.collision = entity.move(movement, tiles, enitiies)

    def phys_block(self, entity, player, tiles, enitiies, pl_movement, dt):
        if entity.name == 'pblock':
            movement = [0, 0]
            if (player.collision['left']['name'] == entity.name and player.collision['left']['id'] == entity.id) or (
                    player.collision['right']['name'] == entity.name and player.collision['right']['id'] == entity.id):
                movement[0] = pl_movement[0]

            entity.y_momentum += 20 * dt
            if entity.y_momentum > 3:  # Максимальная скорость падения
                entity.y_momentum = 3
            if entity.y_momentum < -6:  # Максимальная скорость прыжка
                entity.y_momentum = -6
            movement[1] = round(entity.y_momentum)
            entity.collision = entity.move(movement, tiles, enitiies)


class GUI():
    def __init__(self):
        self.sprites = []
        self.font = pg.font.Font(None, 32)

    def entity_HP(self, rect, camera, hp):
        hp_rect = pg.Rect(rect.x - camera[0] + 1, rect.y - camera[1] - 4, int(0.14 * hp), 1)
        pg.draw.rect(display, 'red', hp_rect)

    def message(self, data_dict):
        for tag in data_dict:
            text, pos, color, font, show, alpha = data_dict[tag]['text'], data_dict[tag]['pos'], data_dict[tag]['color'], \
                data_dict[tag]['font'], data_dict[tag]['show'], data_dict[tag]['alpha']
            if show:
                surf = font.render(str(text), False, color)
                surf.set_alpha(alpha)
                rect = surf.get_rect(topleft=pos)
                screen.blit(surf, rect)


class Physics():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def __test_collide(self, tiles=None, entities=None):
        hit_list = []

        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile[1]) and self.rect != tile[1]:
                    dict = {'rect': tile[1], 'name': 'tile', 'id': 0}
                    hit_list.append(dict)
        if entities:
            for entity in entities:
                if self.rect.colliderect(entity.obj.rect) and entity.iscollision and self.rect != entity.get_rect():
                    dict = {'rect': entity.obj.rect, 'name': entity.name, 'id': entity.id}
                    hit_list.append(dict)
        return hit_list

    def move(self, movement, tiles=None, entities=None):
        collision_type = {'top': {'collided': False, 'name': None, 'id': -1},
                          'bottom': {'collided': False, 'name': None, 'id': -1},
                          'left': {'collided': False, 'name': None, 'id': -1},
                          'right': {'collided': False, 'name': None, 'id': -1}}
        normal_tiles = [tile for tile in tiles if len(tile) == 2]
        ramps = [tile for tile in tiles if len(tile) > 2]

        # X-axis
        self.rect.x += int(movement[0])
        hit_list = self.__test_collide(normal_tiles, entities)
        for hit in hit_list:
            if movement[0] > 0:  # movement[0] > 0
                self.rect.right = hit['rect'].left
                collision_type['right']['collided'] = True
                collision_type['right']['name'] = hit['name']
                collision_type['right']['id'] = hit['id']
            if movement[0] < 0:  # movement[0] < 0
                self.rect.left = hit['rect'].right
                collision_type['left']['collided'] = True
                collision_type['left']['name'] = hit['name']
                collision_type['left']['id'] = hit['id']

        # Y-axis
        self.rect.y += int(movement[1])
        hit_list = self.__test_collide(normal_tiles, entities)
        for hit in hit_list:
            if movement[1] > 0:
                self.rect.bottom = hit['rect'].top
                collision_type['bottom']['collided'] = True
                collision_type['bottom']['name'] = hit['name']
                collision_type['bottom']['id'] = hit['id']
            if movement[1] < 0:
                self.rect.top = hit['rect'].bottom
                collision_type['top']['collided'] = True
                collision_type['top']['name'] = hit['name']
                collision_type['top']['id'] = hit['id']

        # RAMPS
        if ramps:
            for ramp in ramps:
                hit_box = ramp[1]
                TILE_SIZE = 16
                if self.rect.colliderect(hit_box):
                    rel_x = (self.rect.x - hit_box.x)
                    if ramp[2] == 1:
                        pos_height = rel_x + self.rect.width
                    if ramp[2] == 2:
                        pos_height = TILE_SIZE - rel_x

                    pos_height = min(pos_height, TILE_SIZE)
                    pos_height = max(pos_height, 0)

                    target_y = hit_box.y + TILE_SIZE - pos_height

                    if self.rect.bottom > target_y:
                        self.rect.bottom = target_y
                        collision_type['bottom']['collided'] = True
                        collision_type['bottom']['name'] = 'ramp'
                        collision_type['bottom']['id'] = ramp[2]

        return collision_type


class Entity():
    def __init__(self, name, x, y, width, height, image=None, iscollision=True, id=0):
        self.name = name
        self.id = id
        self.obj = Physics(x, y, width, height)
        self.collision = {'top': {'collided': False, 'name': None, 'id': -1},
                          'bottom': {'collided': False, 'name': None, 'id': -1},
                          'left': {'collided': False, 'name': None, 'id': -1},
                          'right': {'collided': False, 'name': None, 'id': -1}}
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
        self.particles = []
        self.screen_shake_timer = 0

        self.image_to_render = pg.Surface((self.get_size()))  # DELETE

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
            self.image_to_render = image_to_render  # DELETE


class Button:
    def __init__(self, pos, img_front, img_back=False, inx=-1):
        self.image = img_front
        self.image_back = img_back
        self.rect = self.image.get_rect(topleft=pos)

        self.inx = inx
        self.clicked = False

    def draw(self, display):
        image_to_render = self.image
        action = False
        m_pos = pg.mouse.get_pos()[0] // SCALE, pg.mouse.get_pos()[1] // SCALE
        m_pressed = pg.mouse.get_pressed()[0]

        if self.rect.collidepoint(m_pos):
            if m_pressed:
                image_to_render = self.image_back
            if m_pressed and not self.clicked:
                self.clicked = True

        if self.rect.collidepoint(m_pos):
            if not m_pressed and self.clicked:
                image_to_render = self.image
                self.clicked = False
                action = True

        display.blit(image_to_render, self.rect)
        return action


class Trigger:
    def __init__(self, pos, size, inx, color=(0, 0, 255)):
        self.pos = pos
        self.size = size
        self.rect = pg.Rect(pos, size)
        self.inx = inx

        self.color = color

    def set(self, entity):
        if self.rect.colliderect(entity.get_rect()):
            return True
        else:
            return False

    def show_trigger(self, surf, offset):
        rect = pg.Rect(self.rect.topleft - offset, self.rect.size)
        pg.draw.rect(surf, self.color, rect)
