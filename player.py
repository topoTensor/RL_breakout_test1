import pygame as pg

class Player:
    def __init__(self, WIN_W, WIN_H, speed=30):
        self.dx=1
        self.speed = speed
        
        self.rect = pg.Rect(WIN_W//2-64,WIN_H-32-16, 128, 32)

    def update_pos(self, WIN_W, WIN_H):
        self.rect.x += self.dx*self.speed

        if self.rect.x+self.rect.w+self.dx >= WIN_W:
            self.rect.x = WIN_W-self.rect.w
        elif self.rect.x-self.dx <= 0:
            self.rect.x = 0
        