import os
from typing import Any
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, RandomSampler


class MyDataset(Dataset):

    def __init__(self, file_path, is_train=False, is_ratio=False) -> None:
        super(MyDataset).__init__()
        data_list_all = pd.read_excel(file_path, sheet_name=None, keep_default_na=False)
        # print(f"所有表格名称： {list(data_list_all)}")

        # 数字经济
        x_data_list = data_list_all[list(data_list_all)[1]]
        '''
        ['百度指数热度', '数字普惠金融指数', '每百人互联网用户数', '每百人移动电话用户数',
         '光缆线路长度(公里)', '移动电话交换机容量(万户)', '计算机服务和软件从业人员占比', '人均电信业务总量']
        '''
        self.x_title = [i for i in x_data_list.values[0] if i != '']
        self.x_datas = x_data_list.values[2:]

        # 制造业
        y_data_list = data_list_all[list(data_list_all)[2]]
        '''
        ['规模以上工业企业R&D经费(万元)', '规模以上工业企业R&D人员全时当量(人年)', '城镇化率', 
         '产业结构合理化', '单位水产出价值', '单位二氧化硫产出价值', '市场化程度', '规模以上工业企业利息支出',
         '制造业劳动报 酬水平与平均之比', '民生财政支出']
        '''
        self.y_title = [i for i in y_data_list.values[0] if i != '']
        self.y_datas = y_data_list.values[2:]

        self.position = self.x_datas[:, 0].astype(float) / 1000000
        self.position = np.expand_dims(self.position, 1)
        # 标准化值
        self.x_datas = self.x_datas[:, 5::3].astype(float)
        self.y_datas = self.y_datas[:, 5::3].astype(float)

        # 地理位置当作变量
        self.x_datas = np.hstack([self.position, self.x_datas])

    def __len__(self):
        assert len(self.x_datas) == len(self.y_datas)
        return len(self.y_datas)

    def __getitem__(self, index: Any) -> Any:
        x = torch.from_numpy(self.x_datas[index]).to(torch.float32)
        y = torch.from_numpy(self.y_datas[index]).to(torch.float32)
        return x, y


def get_dataset(file_path,batch_size):
    train_dataset = MyDataset(file_path, is_train=True)
    test_dataset = MyDataset(file_path, is_train=False)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)

    return train_loader, test_loader


if __name__ == "__main__":
    mydataset = MyDataset(r'datasets\调用数据库.xlsx')