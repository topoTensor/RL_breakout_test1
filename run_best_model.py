import pygame as pg
import torch
from env import Environment
import random


WIN_W = 1280  
WIN_H = 720

BLOCK_W = 64
BLOCK_H = 32

padding_w = 32
padding_h = 32
block_dist_w=16
block_dist_h=16


best_model = Environment(WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h).net
best_model.load_state_dict(torch.load('best_model.pth'))
best_model.eval()
print("Model loaded to best_model.pth")

pg.init()

# Initialize pygame for visual run
screen = pg.display.set_mode((WIN_W, WIN_H))
pg.display.set_caption("Best Agent Demo")
clock = pg.time.Clock()

# Create a single environment using the best model
test_env = Environment(WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h)
test_env.restart(WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h)
test_env.ball.speed = random.uniform(10,15)
test_env.net.load_state_dict(best_model.state_dict())
test_env.running = True

# Visual run loop 
visual_running = True
while visual_running and test_env.running:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            visual_running = False

    test_env.update(WIN_W, WIN_H)

    # Draw blocks
    for block in test_env.blocks:
        pg.draw.rect(screen, (0, 200, 255), block)

    # Draw paddle and ball
    pg.draw.rect(screen, (255, 255, 255), test_env.player.rect)
    pg.draw.rect(screen, (255, 0, 0), test_env.ball.rect)

    # display score
    font = pg.font.SysFont(None, 24)
    score_text = font.render(f"Score: {test_env.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pg.display.flip()
    clock.tick(60)

pg.quit()
print(f"Agent finished with score: {test_env.score}")
