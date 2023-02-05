import pygame as pg
from Settings import *
import Engine as E


class TestLevel():
    def __init__(self):
        self.objectA = E.Entity('entity_test', 100, 100, 100, 100)
        self.speed = 150

        self.tiles = [pg.Rect(0, 200, 1000, 100)]
        self.camera = [0, 0]

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
        movement = int(movement[0]), int(movement[1])
        return movement
    def play(self, display, dt):

        #self.camera = int(self.objectA.get_pos()[0]-WIN_RES[0]//2+self.objectA.get_size()[0]//2), int(self.objectA.get_pos()[1]-WIN_RES[1]//2+self.objectA.get_size()[1]//2)

        movement = self.player_input(dt, self.objectA)
        self.objectA.move(movement, self.tiles)
        self.objectA.render(display, dt,self.camera)

        for tile in self.tiles:
            pg.draw.rect(display, 'darkgreen', (tile.x-self.camera[0], tile.y-self.camera[1], tile.w, tile.h))
