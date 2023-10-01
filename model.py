import torch
import torch.nn as nn
import torch.nn.functional as F


class MyMLP(nn.Module):

    def __init__(self, in_channel, out_channel, hidden_size):
        super(MyMLP, self).__init__()
        self.linear1 = nn.Linear(in_channel,hidden_size)
        self.linear2 = nn.Linear(hidden_size,hidden_size)
        self.linear3 = nn.Linear(hidden_size,out_channel)

    def forward(self, x):
        x = self.linear1(x)
        x = nn.ReLU()(x)
        x = self.linear2(x)
        x = nn.ReLU()(x)
        x = self.linear3(x)
        return x