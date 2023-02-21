import random
import sys

import pygame as pg
from Settings import *

import Engine as E


class Menu():
    def __init__(self):
        self.sprite = pg.image.load('assets/sprites/Menu.png').convert_alpha()
        self.font = pg.font.Font(None, 32)
        self.color = 'white'

    def exit_button(self):

        surf = self.font.render('Выход', False, self.color)
        rect = surf.get_rect(topleft=(129, 130))

        if rect.collidepoint(E.get_mouse_pos()):
            self.color = 'red'
            if pg.mouse.get_pressed()[0]:
                pg.quit()
                sys.exit()
        else:
            self.color = 'white'
        display.blit(surf, rect)


    def play(self, display, dt):
        display.blit(self.sprite, (0, 0))
        self.exit_button()




