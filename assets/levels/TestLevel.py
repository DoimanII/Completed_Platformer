import pygame as pg
from Settings import *
import Engine as E


class TestLevel():
    def __init__(self):
        self.objectA = E.Physics(100, 100, 100, 100)
        self.speed = 300

        self.tiles = [pg.Rect(300, 100, 100, 100)]

    def player_input(self, dt):
        movement = [0, 0]
        if keys['right']:
            movement[0] = self.speed * dt
        if keys['left']:
            movement[0] = -self.speed * dt
        if keys['up']:
            movement[1] = -self.speed * dt
        if keys['down']:
            movement[1] = self.speed * dt
        return movement

    def play(self, display, dt):

        movement = self.player_input(dt)
        self.objectA.move(movement, self.tiles)

        pg.draw.rect(display, 'darkred', self.objectA.rect)
        for tile in self.tiles:
            pg.draw.rect(display, 'darkgreen', tile)
