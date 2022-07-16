import numpy as np

import torch
import torch.nn as nn
from torch import FloatTensor

from shapely.geometry import Point, LineString
from shapely.ops import nearest_points, split

from .neural_network import Network

class Agent():

    def __init__(self,n, start_pos, timestep, means = None, stds = None):

        self.id = n
        self.is_dead = False

        self.position = np.array(start_pos)
        self.velocity = np.random.rand(2)*np.array((3,np.random.choice((-1,1))))
        self.dt = timestep

        self.n_sight_lines = 8
        self.distances = np.zeros(self.n_sight_lines)
        self.sight_lines = [ [] for _ in range(self.n_sight_lines) ]

        self.neuron_structure = [10,16,4,2]
        self.calculate_cumulative_neurons()
        self.network = Network(self.neuron_structure)

        if means != None and stds != None:
            self.custom_initialize_weights(means, stds)

    def move(self, track):

        acceleration = self.network.forward(torch.cat((FloatTensor(self.distances),FloatTensor(self.velocity))))

        self.velocity = self.dt * acceleration.detach().numpy()

        self.position += self.dt*self.velocity

        if not track.track.contains(Point(self.position)):
            self.is_dead = True
        
        else:
            self.calculate_surroundings(track)

    def on_center_line(self,track):

        ag_end = Point(self.position)
        pos_on_line, _ = nearest_points(track.center_line_shapely,ag_end)

        return(list(pos_on_line.coords)[0])

    def calculate_surroundings(self,track):

        angles = np.arange(0,2*np.pi,2/self.n_sight_lines*np.pi)
        position = Point(self.position)

        for i,angle in enumerate(angles):

            direction = np.array((np.sin(angle),np.cos(angle)))
            aux_point = (self.position+2000*direction)
            aux_line = LineString([self.position,aux_point])
            intersections = track.track.exterior.intersection(aux_line)
            distance = position.distance(intersections)

            if intersections.geom_type == 'Point':
                self.sight_lines[i] = [self.position,list(intersections.coords)[0]]

            else:
                self.sight_lines[i] = [self.position,self.position+distance*direction]
            
            self.distances[i] = distance

    def calculate_cumulative_neurons(self):

        self.cumulative_neurons = [0]
        cumulative = 0
        for i in range(len(self.neuron_structure)-1): 
            layer_tot = self.neuron_structure[i]*self.neuron_structure[i+1]\
                        +self.neuron_structure[i+1]
            self.cumulative_neurons.append(layer_tot + cumulative)
            cumulative += layer_tot
    
    def custom_initialize_weights(self, means, stds):

        weights = torch.normal(mean=means, std = stds)
        neur = self.neuron_structure

        for i,layer in enumerate(self.network.layers):

            start = self.cumulative_neurons[i]

            layer_weight = torch.reshape(weights[start:start+neur[i]*neur[i+1]],(neur[i+1],neur[i]))
            layer.weight = nn.Parameter(layer_weight)
            layer.bias = nn.Parameter(weights[start+neur[i]*neur[i+1]:start+neur[i]*neur[i+1]+neur[i+1]])