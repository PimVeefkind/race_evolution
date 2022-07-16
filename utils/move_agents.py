import pygame

from utils.constants import agent_color, sight_color

def move_agents(screen,track, agents, alive_agents):

    for i,id in enumerate(alive_agents):

        agent = agents[id]

        agent.move(track)

        if agent.is_dead:
            alive_agents.remove(id)

        #for i,new_sight in enumerate(agent.sight_lines):

        #    pygame.draw.line(screen, sight_color, new_sight[0],new_sight[1],1)

        pygame.draw.circle(screen, agent_color, agent.position, radius=3)

    return alive_agents
