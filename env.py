from ball import Ball
from player import Player
import torch
import random
from NN import NN
import pygame as pg


class Environment:
    def __init__(self, WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h):

        self.blocks = []

        #init blocks
        for i in range((WIN_W - padding_w * 2) // (BLOCK_W+block_dist_w)):
            for j in range((WIN_H - padding_h * 2) // (BLOCK_H+block_dist_h)//2):
                self.blocks.append(pg.Rect(padding_w + i * (BLOCK_W+block_dist_w), padding_h + j * (BLOCK_H+block_dist_h), BLOCK_W, BLOCK_H))

        self.player = Player(WIN_W, WIN_H)
        self.ball = Ball(WIN_W, WIN_H, speed=10)
        self.running = False

        self.ball.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.ball.dy = -random.uniform(0.5, 1.5)

        self.score = 0

        self.info = (self.player.rect.x, self.player.dx, self.ball.rect.x, self.ball.rect.y, self.ball.dx, self.ball.dy)
        self.net = NN(len(self.info), 4,4, 1)

    def restart(self, WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h):
        self.blocks = []

        #init blocks
        for i in range((WIN_W - padding_w * 2) // (BLOCK_W+block_dist_w)):
            for j in range((WIN_H - padding_h * 2) // (BLOCK_H+block_dist_h)//2):
                self.blocks.append(pg.Rect(padding_w + i * (BLOCK_W+block_dist_w), padding_h + j * (BLOCK_H+block_dist_h), BLOCK_W, BLOCK_H))

        self.player = Player(WIN_W, WIN_H)
        self.player.rect.x = random.uniform(0, WIN_W)

        self.ball = Ball(WIN_W, WIN_H, speed=random.uniform(3, 10))

        self.ball.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.ball.dy = -random.uniform(0.5, 1.5)
        
        self.running = False

        self.score = 0
        self.info = (self.player.rect.x, self.player.dx, self.ball.rect.x, self.ball.rect.y, self.ball.dx, self.ball.dy)


    def update(self, WIN_W, WIN_H):
        #update ball & blocks
        if self.running:
            prev_rect = self.ball.rect.copy()

            self.ball.rect.x += self.ball.dx*self.ball.speed
            self.ball.rect.y += self.ball.dy*self.ball.speed

            for b in self.blocks:
                if b.colliderect(self.ball.rect):
                    if prev_rect.right <= b.left or prev_rect.left >= b.right:
                        self.ball.dx *= -1
                    if prev_rect.bottom <= b.top or prev_rect.top >= b.bottom:
                        self.ball.dy *= -1
                    self.score += 1
                    self.blocks.remove(b)

            if self.player.rect.colliderect(self.ball.rect):
                self.ball.dy *= -1

            if self.ball.rect.y > WIN_H:
                self.running = False

            self.ball.bounce_walls(WIN_W)
            
            #update self.player position
            self.info = (self.player.rect.x, self.player.dx, self.ball.rect.x, self.ball.rect.y, self.ball.dx, self.ball.dy)
            self.info = torch.tensor(self.info)
            self.info = self.info.to(torch.float32)
            self.player_dx=self.net.forward(self.info).item()

            self.player.dx = self.player_dx
            self.player.update_pos(WIN_W,WIN_H)

            self.score += 0.01  # reward for surviving