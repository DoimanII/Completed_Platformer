import pygame as pg
pg.init()
font = pg.font.Font(None, 32)

def debug(info, display):
    surf = font.render(str(info), False, 'white')
    rect = surf.get_rect(topleft=(15, 15))

    pg.draw.rect(display, 'black', rect)
    display.blit(surf, rect)