import pygame

import numpy as np

from utils.agent import Agent
from utils.build_track import Track
from utils.move_agents import move_agents
from utils.calculate_final_scores import calculate_final_scores
from utils.constants import track_color, background_color, center_color

screen_size = np.array([800,600])
pygame.init()
screen = pygame.display.set_mode(screen_size)

n_elements = 6
narrowness = 0.2
track = Track(n_elements, narrowness, screen_size)

timestep = 0.2
n_agents = 5
agents = []
alive_agents = list(np.arange(n_agents))
for n in range(n_agents):
    agent = agents.append(Agent(n,track.starting_position, timestep))

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calculate_final_scores(track, agents)
            gameOn = False
    
    screen.fill(background_color)

    pygame.draw.polygon(screen, color = track_color, points = track.exterior_list)

    move_agents(screen,track, agents, alive_agents)
    
    pygame.draw.lines(screen, color = center_color, closed = False,points = track.center_list)


    pygame.display.update()