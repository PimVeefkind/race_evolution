import pygame

import numpy as np

from utils.agent import Agent
from utils.build_track import Track
from utils.move_agents import move_agents
from utils.evolve_agents import evolve_agents
from utils.draw_fixed_elements import draw_fixed_elements

screen_size = np.array([800,600])
pygame.init()
screen = pygame.display.set_mode(screen_size)

n_elements = 6
narrowness = 0.2
track = Track(n_elements, narrowness, screen_size)

timestep = 0.4
n_agents = 100
agents = []
alive_agents = list(np.arange(n_agents))
for n in range(n_agents):
    agent = agents.append(Agent(n,track.starting_position, timestep))

gameOn = True
i = 0
ep_number = 0
max_iter = 1500

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
    
    draw_fixed_elements(screen, track ,i , ep_number)
    alive_agents = move_agents(screen,track, agents, alive_agents)

    if len(alive_agents) == 0 or i == max_iter:

        agents = evolve_agents(agents, track, timestep)
        alive_agents = list(np.arange(n_agents))
        i = 0
        ep_number += 1

    pygame.display.update()
    i+=1