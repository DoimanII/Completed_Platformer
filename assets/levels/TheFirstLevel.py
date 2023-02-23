import random

import pygame as pg
from Settings import *
import Engine as E


class TheFirstLevel():
    def __init__(self):
        self.GUI = E.GUI()
        self.tiles, self.world_obj, self.entities, self.player = E.load_level_from_image(
        pg.image.load('assets/levels/maps/level_1.png')) # , self.player

        self.player.collision = {'collision': {'top': False, 'bottom': False, 'left': False, 'right': False},
                                 'name': [None, None]}

        self.BG_obg = pg.Rect(300, 50, 25, 25)


    def simple_player_animation(self, movement, entity):
        if movement[0] == 0:
            entity.action = 'idle'
            entity.animation_speed = 1
        if movement[0] != 0:
            entity.action = 'walk'
            entity.animation_speed = 6


    def player_input(self, dt, entity, collision):
        movement = [0, 0]
        self.player.y_momentum += 20 * dt

        if keys['right']:
            movement[0] = self.player.speed * dt
            entity.flip_x = True
        if keys['left']:
            movement[0] = -self.player.speed * dt
            entity.flip_x = False
        if keys['up'] and collision['bottom']:
            if self.player.air_timer < 10:
                self.player.y_momentum = - self.player.jump_height * dt

        movement[1] = self.player.y_momentum
        if self.player.y_momentum > 3:
            self.player.y_momentum = 3
        return movement

    def player_update(self, dt):
        # movement
        movement = self.player_input(dt, self.player, self.player.collision['collision'])
        # move and jump
        self.player.collision = self.player.move(movement, self.tiles, self.entities)
        if self.player.collision['collision']['bottom'] or self.player.collision['collision']['top']:
            self.player.y_momentum = 1
            if self.player.air_timer > 1:
                self.player.HP -= 10 + int(self.player.air_timer * 20)
            self.player.air_timer = 0
        else:
            self.player.air_timer += 1 * dt

        # animation
        self.simple_player_animation(movement, self.player)
        # camera
        camera = E.simple_camera(self.player.get_rect(), display)

        return camera, movement

    def play(self, display, dt):
        camera, movement = self.player_update(dt)

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

