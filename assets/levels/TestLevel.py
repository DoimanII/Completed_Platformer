import pygame as pg
from Settings import *
import Engine as E



class TestLevel():
    def __init__(self):
        self.objectA = E.Entity('entity_test', 100, 0, 100, 100)
        self.speed = 300

        self.camera = [0, 0]
        self.map = [
                    ['H', '-', 'H', '-', 'H', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['%', '-', '%', '-', '%', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['-', '-', '-', '-', '-', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['%', '-', '%', '-', '%', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['-', '-', '-', '-', '-', '-', ' ', ' ', 'b', ' ', 't', ' ', ' ', 'p', 'p', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', 't', ' ', ' ', ' ', ' ', ' '],
                    ['%', '-', '%', '-', '%', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-', 'G', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-', '%', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
                    ]
        self.tiles, self.world_obj, self.entities = E.load_level(self.map)

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
        movement = movement[0], movement[1]
        return movement
    def play(self, display, dt):

        movement = self.player_input(dt, self.objectA)
        self.camera = int(self.objectA.get_pos()[0]-WIN_RES[0]//2+self.objectA.get_size()[0]//2), int(self.objectA.get_pos()[1]-WIN_RES[1]//2+self.objectA.get_size()[1]//2)

        self.objectA.move(movement, self.tiles)
        self.objectA.render(display, dt,self.camera)

        for tile in self.tiles:
            rect = (tile[1].x-self.camera[0], tile[1].y-self.camera[1], tile[1].w, tile[1].h)
            sprite = tile_database[tile[0]]
            display.blit(sprite, rect)

        for obj in self.world_obj:
            rect = (obj[1].x-self.camera[0], obj[1].y-self.camera[1], obj[1].w, obj[1].h)
            sprite = tile_database[obj[0]]
            display.blit(sprite, rect)

