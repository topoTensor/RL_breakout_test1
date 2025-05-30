import pygame as pg
from env import Environment
from ball import Ball
from player import Player

import torch
import random
from NN import NN

import time

pg.init()

WIN_W = 1280  
WIN_H = 720

BLOCK_W = 64
BLOCK_H = 32

padding_w = 32
padding_h = 32
block_dist_w=16
block_dist_h=16

num_envs=500
envs = []

for i in range(num_envs):
    envs.append(Environment(WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h))

for env in envs:
    env.running = True

# notes
# 1. the speed of the ball and its direction are randomly generated at every restart
# 2. initial x position of the player is randomly generated at every restart
# 3. number of environments makes a huge difference in training speed

# game loop
run_sim = True
epochs = 0
break_epochs = 8
best_score = 0
best_model_i=0
best_model = None
start_time = time.time()
termination_score = 1000
while run_sim:

    num_runs = num_envs
    for env in envs:
        env.update(WIN_W, WIN_H)
        if env.running==False:
            num_runs-=1

        # in order to avoid the model being stuck in a loop, we will terminate the run if the score is too high
        if env.score > termination_score:
            env.running = False

    if num_runs == 0:
        for i, env in enumerate(envs):
            if env.score > best_score:
                best_model = env.net
                best_model_i = i
                best_score = env.score
                avg_score = sum(env.score for env in envs) / num_envs
                print(f"Best: {best_score:.2f}, Avg: {avg_score:.2f}")
                epochs += 1

        for i, env in enumerate(envs):
            env.net.load_state_dict(best_model.state_dict())

            if i != best_model_i:
                env.net.mutate(mutation_rate=1.0, mutation_strength=0.5)

            env.restart( WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h)
        
        if best_score > termination_score:
            break

        for env in envs:
            env.running = True
        

torch.save(best_model.state_dict(), "best_model.pth")
print("Model saved to best_model.pth")

# Initialize pygame for visual run
screen = pg.display.set_mode((WIN_W, WIN_H))
pg.display.set_caption("Best Agent Demo")
clock = pg.time.Clock()

# Create a single environment using the best model
test_env = Environment(WIN_W, WIN_H, BLOCK_W, BLOCK_H, padding_w, padding_h, block_dist_w, block_dist_h)
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
