import random

import pygame as pg
from Settings import *
import Engine as E


class Sample():
    def __init__(self):
        self.GUI = E.GUI()
        self.user = E.User()
        self.EA = E.EntityAssets()

        self.level_name = 'TheFirstLevel'
        self.text = {'player_name':{'text': ' player', 'pos': (0, 0), 'color': 'white', 'font': pg.font.Font(None, 24), 'show': True}}
        self.check_point = [272, 736]


        self.tiles, self.world_obj, self.entities, self.background, self.player = E.load_level_from_image(
        pg.image.load('assets/levels/maps/level_0.png'))


    def play(self, display, dt):
        movement = self.user.user_input(self.player, self.tiles, self.entities, dt, self.check_point)
        camera = self.user.simple_camera(self.player.get_rect(), display)

        # BackGround render
        for BG in self.background:
            rect = (int(BG[0].x - camera[0] * BG[1]), int(BG[0].y - camera[1] * BG[1]), *BG[0].size)
            color = BG[2]
            pg.draw.rect(display, color, rect)

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
            self.EA.spikes(entity, self.player, dt)
            self.EA.bush(entity, self.player, dt)
            self.EA.falling_block(entity, self.player, self.tiles, self.entities, dt)
            self.EA.phys_block(entity, self.player, self.tiles, self.entities, movement, dt)


        # render player
        self.player.render(display, dt, camera)
        self.GUI.entity_HP(self.player.get_rect(), camera, self.player.HP)

        self.text['player_name']['pos'] = (self.player.get_pos()[0] - camera[0]) * SCALE, (
                    self.player.get_pos()[1] - 9 - camera[1]) * SCALE
