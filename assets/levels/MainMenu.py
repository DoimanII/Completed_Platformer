import random
import sys

import pygame as pg
from Settings import *
import Engine as E


class MainMenu():
    def __init__(self):
        # Main game init
        self.GUI = E.GUI()
        self.change_level_to = None
        self.new_game = False

        # others
        self.text = {'b_continue': {'text': 'Продолжить', 'pos': ((75 + 38 - 32) * SCALE, (40 + 12 - 5) * SCALE),
                                    'color': 'white', 'font': pg.font.Font(None, 64), 'show': True, 'alpha': 255},
                     'b_new': {'text': 'Новая игра', 'pos': ((75 + 38 - 32) * SCALE, (40 + 32 + 12 - 5) * SCALE),
                               'color': 'white', 'font': pg.font.Font(None, 64), 'show': True, 'alpha': 255},
                     'b_exit': {'text': 'Выход', 'pos': ((75 + 38 - 32) * SCALE, (40 + 64 + 12 - 5) * SCALE),
                                'color': 'white', 'font': pg.font.Font(None, 64),
                                'show': True, 'alpha': 255},
                     'info': {'text': 'F3 - подсказки', 'pos': (screen.get_width()-200, screen.get_height()-24),
                                'color': 'white', 'font': pg.font.Font(None, 24),
                                'show': True, 'alpha': 120}
                     }
        self.background = [[pg.Rect(50, 10, 64, 512), 0.35, (55, 148, 110, 255)],
                           [pg.Rect(400, 15, 64, 512), 0.35, (55, 148, 110, 255)],
                           [pg.Rect(200, 30, 48, 512), 0.5, (63, 181, 133, 255)],
                           [pg.Rect(355, 35, 48, 512), 0.5, (63, 181, 133, 255)],
                           [pg.Rect(25, 55, 48, 512), 0.5, (63, 181, 133, 255)],
                           [pg.Rect(450, 55, 48, 512), 0.5, (63, 181, 133, 255)]]  #

        # Buttons
        self.buttons = [E.Button((75, 40 + 32 * i), tile_database['BlueButtonUp'], tile_database['BlueButtonDown'], i)
                        for i in range(3)]  # img, rect

        # Camera
        self.offset = pg.math.Vector2(150, 0)
        self.camera_boarders = {'left': 55, 'right': 55, 'top': 0, 'bottom': 0}
        self.camera_speed = 100
        self.BG_img = pg.transform.scale(tile_database['MenuBG'], (768, 192 * 0.9))

    def find_offset(self, dt):
        m_pos = pg.math.Vector2(pg.mouse.get_pos()[0] // SCALE, pg.mouse.get_pos()[1] // SCALE)
        if self.offset.x > 1 and m_pos.x <= self.camera_boarders['left']:
            self.offset.x += -self.camera_speed * dt
        if self.offset.x < 445 and m_pos.x >= WIN_RES[0] - self.camera_boarders['right']:
            self.offset.x += self.camera_speed * dt

        if self.offset.x > 446:
            self.offset.x = 445
        elif self.offset.x < 1:
            self.offset.x = 0

    def draw_background(self):
        for BG in self.background:
            rect = (int(BG[0].x - self.offset.x * BG[1]), int(BG[0].y - self.offset.y * BG[1]), *BG[0].size)
            color = BG[2]
            pg.draw.rect(display, color, rect)

    def main(self, display, last_scene):
        for button in self.buttons:
            if button.draw(display):
                if button.inx == 0:  # Continue
                    self.change_level_to = last_scene
                if button.inx == 1:  # New Game
                    self.new_game = True
                if button.inx == 2:  # EXIT
                    pg.quit()
                    sys.exit()

    def play(self, display, dt, last_scene):
        self.find_offset(dt)

        self.draw_background()
        display.blit(self.BG_img, pg.math.Vector2(0, 192 - 192 * 0.9) - self.offset)
        self.main(display, last_scene)
