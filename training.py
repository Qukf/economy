import torch
import numpy as np
import os
import time

from datasets import get_dataset

train_loader, test_loader = get_dataset(r'datasets\调用数据库.xlsx')


def training():
    for i, (x, y) in enumerate(train_loader):
        print(i, x, y)
        exit()


if __name__ == "__main__":
    training()
