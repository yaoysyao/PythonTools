# -*- coding: utf-8 -*-
# @FileName  :dataDemo.py
# @Time      :2023/1/1 16:40
# @Author    :yaoys
# @Desc      : split train,test,dev data
import pandas as pd

from yaoysTools.data import SplitFiles
from yaoysTools.data.datautil import *

data = pd.read_csv(filepath_or_buffer='../demoFile/data.csv')
print(len(data))

# The test_ratio default is 0.2
# get train and test data
train_data, test_data = split_train_test(data=data)
print(len(train_data), len(test_data), len(train_data) + len(test_data) == len(data))

# The test_ratio default is 0.2
# use sklearn.model_selection train_test_split
# get train and test data
train_data, test_data = split_train_test_sklearn(data=data)
print(len(train_data), len(test_data), len(train_data) + len(test_data) == len(data))

# get train,test,dev data
# The ratio is default 0.6,0.2,0.2,if the data len >10000,the ratio default is 0.8,0.1,0.1
train_data, test_data, dev_data = split_train_test_dev(data=data)
print(len(train_data), len(test_data), len(dev_data), len(train_data) + len(test_data) + len(dev_data) == len(data))

# split file,the file is csv or text,you can get train data and test data
file = SplitFiles(file_path='../demoFile/data.csv', train_data_path='../demoFile/data_train.csv', test_data_path='../demoFile/data_test.csv')
file.splitFile()
file = SplitFiles(file_path='../demoFile/data.txt', train_data_path='../demoFile/data_train.txt', test_data_path='../demoFile/data_test.txt')
file.splitFile()
