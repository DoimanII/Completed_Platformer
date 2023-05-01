import random

import pygame as pg
from Settings import *
import Engine as E


class TheFirstLevel():
    def __init__(self):
        self.GUI = E.GUI()
        self.user = E.User()
        self.EA = E.EntityAssets()

        self.level_name = 'TheFirstLevel'
        self.text = {'player_name':{'text': ' player', 'pos': (0, 0), 'color': 'white', 'font': pg.font.Font(None, 24), 'show': True}}
        self.check_point = [272, 736]

        self.tiles, self.world_obj, self.entities, self.background, self.player = E.load_level_from_image(
        pg.image.load('assets/levels/maps/level_1.png'))
        self.particles = [] # pos, vel, timer

        # camera
        self.offset = pg.math.Vector2()
        self.camera_rect = self.user.camera_rect
        self.camera_rect.center = self.player.get_pos()

    def play(self, display, dt):
        movement = self.user.user_input(self.player, self.tiles, self.entities, dt, self.check_point)
        self.offset.xy = self.user.box_target_camera(self.player.get_rect())


        # BackGround render
        for BG in self.background:
            rect = (int(BG[0].x-self.offset.x*BG[1]), int(BG[0].y-self.offset.y*BG[1]), *BG[0].size)
            color = BG[2]
            pg.draw.rect(display,color, rect)

        # render world_obj
        for wob in self.world_obj:
            rect = (wob[1].x - self.offset.x, wob[1].y - self.offset.y, *wob[1].size)
            image = tile_database[wob[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)


        # render tiles
        for tile in self.tiles:
            rect = (tile[1].x - self.offset.x, tile[1].y - self.offset.y, *tile[1].size)
            image = tile_database[tile[0]]
            if display.get_rect().colliderect(rect):
                display.blit(image, rect)


        # render entity
        for entity in self.entities:
            entity.render(display, dt, self.offset)
            self.EA.spikes(entity, self.player, dt)
            self.EA.bush(entity, self.player, dt)
            self.EA.falling_block(entity, self.player, self.tiles, self.entities, dt)
            self.EA.phys_block(entity, self.player, self.tiles, self.entities,movement,  dt)

        for particle in self.player.particles:

            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            particle[2] -= 0.4
            if particle[2] <= 0:
                self.player.particles.remove(particle)
            pg.draw.rect(display, 'white', (particle[0][0]-self.offset.x, particle[0][1]-self.offset.y, particle[2], particle[2]))

        # render player
        self.player.render(display, dt, self.offset)
        self.GUI.entity_HP(self.player.get_rect(), self.offset, self.player.HP)

        self.text['player_name']['pos'] = (self.player.get_pos()[0]-self.offset.x)*SCALE, (self.player.get_pos()[1]-9-self.offset.y)*SCALE
        if keys['action']:
            self.text['player_name']['color'] = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))

        #pos = self.camera_rect.topleft - self.offset
        #pg.draw.rect(display, 'yellow', (*pos, self.camera_rect.w, self.camera_rect.h), 1)


