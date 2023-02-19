import random

import pygame as pg
from Settings import *
import Engine as E


class Sample():
    def __init__(self):
        self.GUI = E.GUI()
        self.tiles, self.world_obj, self.entities = E.load_level_from_image(pg.image.load('assets/levels/level_map_0.png'))

        self.player = E.Entity('entity_test', 290, 225, 100, 100)
        self.speed = 200
        self.HP = 100
        self.collision = {'collision':{'top': False, 'bottom': False, 'left': False, 'right': False}, 'name':None}
        self.air_timer = 0
        self.player_y_momentum = 0



    def player_input(self, dt, entity, j):
        movement = [0, 0]
        self.player_y_momentum += 0.2

        if keys['right']:
            movement[0] = self.speed * dt
            entity.flip_x = True
        if keys['left']:
            movement[0] = -self.speed * dt
            entity.flip_x = False
        if keys['up'] and j:
            if self.air_timer < 10:
                self.player_y_momentum = - 250 * dt

        movement[1] += self.player_y_momentum
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3
        return movement

    def play(self, display, dt):
        #movement
        movement = self.player_input(dt, self.player, self.collision['collision']['bottom'])
        #move
        self.collision = self.player.move(movement, self.tiles)
        if self.collision['collision']['bottom'] or self.collision['collision']['top']:
            self.player_y_momentum = 1
            self.air_timer = 0
        else:
            self.air_timer += 1

        #camera
        camera = E.simple_camera(self.player.get_rect(), display)

        #render world_obj
        for wob in self.world_obj:
            rect = (wob[1].x - camera[0], wob[1].y-camera[1], *wob[1].size)
            image = tile_database[wob[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)
        #render tiles
        for tile in self.tiles:
            rect = (tile[1].x - camera[0], tile[1].y-camera[1], *tile[1].size)
            image = tile_database[tile[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)
        #render entity
        for entity in self.entities:
            pass

        #render player
        self.player.render(display,dt,camera)
        self.GUI.entity_HP(self.player.get_rect(), camera, 75)


