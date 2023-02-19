import random

import pygame as pg
from Settings import *
import Engine as E


class TestLevel():
    def __init__(self):
        self.objectA = E.Entity('entity_test', 280, 232, 100, 100)
        self.speed = 200
        self.ent = self.objectA.get_rect()
        self.GUI = E.GUI()
        self.HP = 100

        self.tiles, self.world_obj, self.entities = E.load_level_from_image(pg.image.load('assets/levels/level_map_0.png')) #E.load_level(self.map)


    def player_input(self, dt, entity):
        movement = [0, 0]
        if keys['right']:
            movement[0] = self.speed * dt
            entity.flip_x = True
        if keys['left']:
            movement[0] = -self.speed * dt
            entity.flip_x = False
        if keys['up']:
            movement[1] = -self.speed * dt
        if keys['down']:
            movement[1] = self.speed * dt
        return movement

    def play(self, display, dt):

        movement = self.player_input(dt, self.objectA)
        self.objectA.move(movement, self.tiles)
        if keys['action']:
            # self.ent = random.choice([self.world_obj[random.randint(0, len(self.world_obj)-1)][1], self.objectA.get_rect()])
            if self.HP <= 0:
                self.HP = 100
            self.HP -= 1
        camera = E.simple_camera(self.ent, display)

        for tile in self.tiles:
            rect = pg.Rect(tile[1].x - camera[0], tile[1].y - camera[1], tile[1].w, tile[1].h)
            sprite = tile_database[tile[0]]
            if display.get_rect().colliderect(rect):
                display.blit(sprite, rect)

        for obj in self.world_obj:
            rect = pg.Rect(obj[1].x - camera[0], obj[1].y - camera[1], obj[1].w, obj[1].h)
            sprite = tile_database[obj[0]]

            if display.get_rect().colliderect(rect):
                display.blit(sprite, rect)

        self.objectA.render(display, dt, camera)
        self.GUI.entity_HP(self.objectA.get_rect(), camera, self.HP)
