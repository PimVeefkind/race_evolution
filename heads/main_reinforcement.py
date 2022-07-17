import pygame
import os
import sys
import numpy as np

cwd = os.getcwd()
sys.path.insert(0, cwd)

from reinforcement.reinforcement_agent import Agent
from utils.build_track import Track
from reinforcement.reinforcement_take_step import take_step
from evolution.evolve_agents import evolve_agents
from utils.draw_fixed_elements import draw_fixed_elements

screen_size = np.array([800,600])
pygame.init()
screen = pygame.display.set_mode(screen_size)

n_elements = 6
narrowness = 0.2
track = Track(n_elements, narrowness, screen_size)

timestep = 0.4
agent = Agent()

gameOn = True
i = 0
ep_number = 0
max_iter = 500

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
    
    draw_fixed_elements(screen, track ,i , ep_number)
    has_died = take_step(screen,track)

    if has_died or i == max_iter:

        #agent.update_network()
        #agent.reset()
        i = 0
        ep_number += 1

    pygame.display.update()
    i+=1