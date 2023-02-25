import random

import pygame as pg
from Settings import *
import Engine as E


class Sample():
    def __init__(self):
        self.GUI = E.GUI()
        self.tiles, self.world_obj, self.entities, self.player = E.load_level_from_image(
        pg.image.load('assets/levels/maps/level_0.png'))


        self.player.collision = {'collision': {'top': False, 'bottom': False, 'left': False, 'right': False},
                                 'name': None}

        self.BG_obg = pg.Rect(300, 50, 25, 25)

    def simple_player_animation(self, movement, entity):
        if movement[0] == 0:
            entity.action = 'idle'
            entity.animation_speed = 1
        if movement[0] != 0:
            entity.action = 'walk'
            entity.animation_speed = 6

    def player_input(self, dt, entity):
        movement = [0, 0]
        entity.y_momentum += 20 * dt # gravity

        if keys['right']: # key input
            movement[0] = entity.speed * dt
            entity.flip_x = True
        if keys['left']:
            movement[0] = -entity.speed * dt
            entity.flip_x = False
        if keys['up'] and entity.collision['collision']['bottom']:
            if entity.air_timer < 10:
                entity.y_momentum = - entity.jump_height * dt

        movement[1] = entity.y_momentum # max falling speed
        if entity.y_momentum > 3:
            entity.y_momentum = 3

        entity.collision = entity.move(movement, self.tiles, self.entities) # collision
        if entity.collision['collision']['bottom'] or entity.collision['collision']['top']: # If player on ground
            entity.y_momentum = 1
            if entity.air_timer > 1:
                entity.HP -= 10 + int(entity.air_timer * 20)
            entity.air_timer = 0
        else:
            entity.air_timer += 1 * dt

        self.simple_player_animation(movement, entity) # animation

        return movement

    def play(self, display, dt):
        movement = self.player_input(dt, self.player)
        camera = E.simple_camera(self.player.get_rect(), display)

        pg.draw.rect(display, (255, 249, 125), (int(self.BG_obg.x-camera[0]*0.25), int(self.BG_obg.y-camera[1]*0.25), *self.BG_obg.size)) # (55, 148, 100)

        # render world_obj
        for wob in self.world_obj:
            rect = (wob[1].x - camera[0], wob[1].y - camera[1], *wob[1].size)
            image = tile_database[wob[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)

        # render tiles
        for tile in self.tiles:
            rect = (tile[1].x - camera[0], tile[1].y - camera[1], *tile[1].size)
            image = tile_database[tile[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)

        # render entity
        for entity in self.entities:
            entity.render(display, dt, camera)
            if entity.name == self.player.collision['name'][0]:
                if entity.name == 'spikes' and self.player.collision['collision']['bottom'] and entity.id == self.player.collision['name'][1]:
                    self.player.y_momentum -= 450 * dt
                    self.player.HP -= 10


        # render player
        self.player.render(display, dt, camera)
        self.GUI.entity_HP(self.player.get_rect(), camera, self.player.HP)
