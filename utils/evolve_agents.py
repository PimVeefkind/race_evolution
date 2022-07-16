import torch

import numpy as np

from shapely.geometry import Point
from shapely.ops import nearest_points, split

from .agent import Agent

def evolve_agents(agents, track, timestep):

    neuron_list = agents[0].neuron_structure
    final_scores = []
    weights = torch.zeros((len(agents),tot_weights(neuron_list)))

    for i,agent in enumerate(agents):
        
        final_scores.append(calculate_score(agent,track))
        weights[i,:] = get_weights(agent)

    best_performers = np.argsort(final_scores)[len(agents)//2:]
    means = torch.mean(weights[best_performers,:], axis = 0)
    stds = torch.std(weights[best_performers,:], axis = 0)

    new_agents = []

    print(np.mean(final_scores))
    for i in range(len(agents)):

        new_agents.append(Agent(i,track.starting_position, timestep, means=means, stds=stds))

    return new_agents

def calculate_score(agent, track):

    ag_end = Point(agent.position)
    pos_on_line, _ = nearest_points(track.center_line_shapely,ag_end,)
    sub_line = split(track.center_line_shapely, pos_on_line)
    
    return(sub_line[0].length)

def get_weights(agent):

    agent_weights = torch.FloatTensor([])

    for layer in agent.network.layers:
        agent_weights = torch.cat((agent_weights, torch.flatten(layer.weight.detach()),\
                                                  torch.flatten(layer.bias.detach())))

    return agent_weights

def tot_weights(neuron_list):

    temp = 0

    for i in range(len(neuron_list)-1):

        temp += neuron_list[i]*neuron_list[i+1]+neuron_list[i+1]

    return temp