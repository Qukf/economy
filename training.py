import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
import os
import time

from datasets import get_dataset
from model import MyMLP

in_channel = 9
out_channel = 10
hidden_size = 128
train_loader, test_loader = get_dataset(r'datasets\调用数据库.xlsx',32)
model = MyMLP(in_channel, out_channel, hidden_size).cuda()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=0.00001)


def training():
    for epoch in range(100):
        for i, (x, y) in enumerate(train_loader):
            x = x.to(device)
            y = y.to(device)
            pred = model(x)

            loss = torch.abs(y - pred).mean()
            loss.backward()
            if i % 10 == 0:
                print(epoch, loss)
            optimizer.step()
            optimizer.zero_grad()
        if epoch % 10 ==0:
            print(y)
            print(pred)


if __name__ == "__main__":
    training()
