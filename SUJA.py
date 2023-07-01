import random

import pygame as pg
from Settings import *
import Engine as E


class TEST():
    def __init__(self):
        self.GUI = E.GUI()
        self.user = E.User()
        self.EA = E.EntityAssets()

        self.level_return = [None, False, False]
        self.text = {}

        self.offset = pg.math.Vector2()
        self.camera_boarders = {'left':20, 'right':20, 'top':20, 'bottom':20}
        self.camera_rect = pg.Rect(self.camera_boarders['left'], self.camera_boarders['right'], WIN_RES[0]-(self.camera_boarders['left']+self.camera_boarders['right']), WIN_RES[1]-(self.camera_boarders['top']+self.camera_boarders['bottom']))

        self.tiles = []
        for i in range(0, 20):
            image = tile_database['box']
            rect = image.get_rect(center=(random.randint(0, 1280/4), random.randint(0, 720/4)))
            self.tiles.append([image, rect, 0])

        self.tiles.append([tile_database['bush'], tile_database['bush'].get_rect(center=(100, 100)), 1])

    def custom_input(self, rect, speed, dt):

        if keys['right']:  # key input
            rect.centerx += round(speed * dt)
        if keys['left']:
            rect.centerx -= round(speed * dt)
        if keys['up']:
            rect.centery -= round(speed * dt)
        if keys['down']:
            rect.centery += round(speed * dt)

        return rect.center


    def play(self, display, dt):
        #self.offset.xy = self.user.mouse_control_camera()
        for tile in sorted(self.tiles, key=lambda tile: tile[1].centery):
            if tile[2] == 1:
                tile[1].center = self.custom_input(tile[1], 100, dt)
                self.offset.xy = self.user.box_target_camera(tile[1])
            pos = tile[1].x-self.offset.x, tile[1].y-self.offset.y
            display.blit(tile[0], pos)

        pg.draw.rect(display, 'green', self.camera_rect, 1)
