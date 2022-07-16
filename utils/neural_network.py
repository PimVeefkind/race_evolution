import torch
import torch.nn as nn
import torch.nn.functional as F
    
class Network(nn.Module):

    def __init__(self, neurons_list):
        super(Network,self).__init__()

        self.layers = []

        for i in range(len(neurons_list)-1):
            self.layers.append(nn.Linear(neurons_list[i],neurons_list[i+1]))

        self.n_layers = len(self.layers)


    def forward(self, x):

        for i in range(self.n_layers):
            x = self.layers[i](x)
            if not i == self.n_layers-1:
                x = F.relu(x)
            else:
                x = torch.tanh(x) * 3

        return x