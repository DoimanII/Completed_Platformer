import random

import pygame as pg
from Settings import *
import Engine as E

class TheThird():
    def __init__(self):
        self.GUI = E.GUI()
        self.user = E.User()
        self.EA = E.EntityAssets()

        self.change_level_to = None
        self.text = {'player_name':{'text': ' player', 'pos': (0, 0), 'color': 'white', 'font': pg.font.Font(None, 24), 'show': True,'alpha':120},
                     'End':{'text': 'Конец', 'pos': (screen.get_width()//2-2*132, 200), 'color': 'white', 'font': pg.font.Font(None, 128), 'show': False,'alpha':255, 'timer': 4},}


        self.tiles, self.world_obj, self.entities, self.background, self.player, self.triggers = E.load_level_from_image(
        pg.image.load('assets/levels/maps/level_3.png'))
        self.background = sorted(self.background, key=lambda bg_list: type(bg_list[1]) != float)
        self.check_point = [*self.player.get_pos()]

        self.particles = [] # pos, vel, timer, color
        self.tile_map = [str(int(t[1].x/t[1].w)) + ';' + str(int(t[1].y/t[1].h)) for t in self.tiles if t[1].size == (16, 16)]

        # camera
        self.offset = pg.math.Vector2()
        self.camera_rect = self.user.camera_rect
        self.camera_rect.center = self.player.get_pos()

    def play(self, display, dt, last_scene):
        movement = self.user.user_input(self.player, self.tiles, self.entities, dt, self.check_point)
        self.offset.xy = self.user.box_target_camera(self.player.get_rect())

        if self.player.screen_shake_timer > 0:
            self.player.screen_shake_timer -= 1
        if self.player.screen_shake_timer:
            m = 0.5  # Временно!!!!
            self.offset.xy += pg.math.Vector2(random.randint(0, 8*m)-4*m, random.randint(0, 8*m)-4*m) # Временно!!!!

        # BackGround render
        for BG in self.background:
            if type(BG[1]) == float:
                rect = (int((BG[0].x - self.offset.x) * BG[1]), int((BG[0].y - self.offset.y) * BG[1]), *BG[0].size)
                color = BG[2]
                pg.draw.rect(display, color, rect)
            else:
                rect = (int(BG[0].x - self.offset.x), int(BG[0].y - self.offset.y), *BG[0].size)
                img = tile_database[BG[1]]
                if display.get_rect().colliderect(rect):
                    display.blit(img, rect)
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

            self.check_point = entity.get_pos() if self.EA.spawn_point_entity(entity, self.player, self.check_point) else self.check_point

            # particles
            if entity.particles:
                self.particles.extend(entity.particles)
            entity.particles = [p for p in entity.particles if p[2] > 0]

        #remove particle
        self.particles.extend(self.player.particles)
        self.particles = [p for p in self.particles if p[2] > 0]
        self.player.particles = [p for p in self.player.particles if p[2] > 0]

        for particle in self.particles:
            particle[0].x += particle[1].x * dt
            pos_str = str(int(particle[0].x/TILE_SIZE)) + ';' + str(int(particle[0].y/TILE_SIZE))
            if pos_str in self.tile_map:
                particle[1].x *= -0.7
                particle[0].x += particle[1].x * 2

            particle[0].y += particle[1].y * dt
            if pos_str in self.tile_map:
                particle[1].y *= -0.7
                particle[0].y += particle[1].y * 2

            particle[2] -= 0.4
            particle[1].y += 10

            pg.draw.rect(display, particle[3], (particle[0].x-self.offset.x, particle[0].y-self.offset.y, particle[2]*0.5, particle[2]*0.5))

        # Triggers
        for trigger in self.triggers:
            if trigger.set(self.player):

                self.text['End']['show'] = True

        self.text['End']['timer'] -= 1 * dt if self.text['End']['show'] else 0
        self.text['End']['alpha'] -= 50 * dt if self.text['End']['show'] else 0
        if self.text['End']['timer'] <= 0:
            self.text['End']['show'] = False

        # render player
        self.player.render(display, dt, self.offset)
        self.GUI.entity_HP(self.player.get_rect(), self.offset, self.player.HP)
        self.text['player_name']['pos'] = (self.player.get_pos()[0]-self.offset.x)*SCALE, (self.player.get_pos()[1]-9-self.offset.y)*SCALE

        #pos = self.camera_rect.topleft - self.offset
        #pg.draw.rect(display, 'yellow', (*pos, self.camera_rect.w, self.camera_rect.h), 1)