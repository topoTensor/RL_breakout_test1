import pygame as pg

class Ball:
    def __init__(self, WIN_W, WIN_H, speed=3):
        self.dx=1
        self.dy=-1
        self.speed = speed
        
        self.rect = pg.Rect(WIN_W//2,WIN_H//2, 16, 16)

    def bounce_walls(self, WIN_W):
        if self.rect.x+self.rect.w >= WIN_W:
            self.dx = -1
            self.rect.x = WIN_W-self.rect.w
        elif self.rect.x <= 0:
            self.dx = 1
            self.rect.x = 0
        if self.rect.y <= 0:
            self.dy = 1
            self.rect.y = 0