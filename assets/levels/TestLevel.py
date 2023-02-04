import pygame as pg
from Settings import *
import Engine as E


class TestLevel():
    def __init__(self):
        self.objectA = E.Entity('entity_test', 100, 100, 100, 100)
        self.speed = 300

        self.tiles = [pg.Rect(150, 100, 100, 100)]

    def player_input(self, dt, entity=None):
        movement = [0, 0]
        if keys['right']:
            movement[0] = self.speed * dt
            if entity != None:
                entity.flip_x = True
        if keys['left']:
            movement[0] = -self.speed * dt
            if entity != None:
                entity.flip_x = False
        if keys['up']:
            movement[1] = -self.speed * dt
        if keys['down']:
            movement[1] = self.speed * dt
        return movement

    def play(self, display, dt):

        movement = self.player_input(dt, self.objectA)
        camera = (int(self.objectA.get_pos()[0]-WIN_RES[0]/2+self.objectA.get_size()[0]/2), int(self.objectA.get_pos()[1]-WIN_RES[1]/2+self.objectA.get_size()[1]/2))
        self.objectA.move(movement, self.tiles)
        self.objectA.render(display, dt,camera)


        for tile in self.tiles:
            pg.draw.rect(display, 'darkgreen', (tile.x-camera[0], tile.y-camera[1], tile.w, tile.h))
