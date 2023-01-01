import numpy as np
import pandas
from sklearn.model_selection import train_test_split


# 自定义划分测试数据集与训练数据集
def split_train_test(data, test_ratio=0.2):
    """
    :param
    data: 数据
    test_ratio:测试数据集的比例，默认0.2，按照2-8原则划分
    """

    if not isinstance(data, pandas.DataFrame):
        raise Exception('please use pandas read_csv read the file')

    # 设置随机数种子，保证每次生成的结果都是一样的
    np.random.seed(42)
    # permutation随机生成0-len(data)随机序列
    shuffled_indices = np.random.permutation(len(data))
    # test_ratio为测试集所占的半分比
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    # iloc选择参数序列中所对应的行
    return data.iloc[train_indices], data.iloc[test_indices]


def split_train_test_dev(data, train_ratio=0.6, test_ratio=0.2, dev_ratio=0.2, random_state=42):
    '''
    划分数据集为训练数据集，测试数据集，验证数据集，默认为6:2:2
    '''
    if not isinstance(data, pandas.DataFrame):
        raise Exception('please use pandas read_csv read the file')
    if train_ratio + test_ratio + dev_ratio != 1:
        raise Exception('The ratio count must is 1')
    # 如果数据集长度大于万级别以上，就按照8:1:1划分
    if len(data) >= 10000:
        train_ratio = 0.8
        test_ratio = 0.1
        dev_ratio = 0.1
    # 设置随机数种子，保证每次生成的结果都是一样的
    np.random.seed(random_state)
    # permutation随机生成0-len(data)随机序列，打乱所有数据的顺序，得到的是随机排序的数组
    shuffled_indices = np.random.permutation(len(data))
    # train_ratio为训练集所占的百分比
    train_set_size = int(len(data) * train_ratio)
    # 从开始到训练数据集长度为训练数据集
    train_indices = shuffled_indices[:train_set_size]
    # 训练数据集到训练+测试为测试数据集
    test_indices = shuffled_indices[train_set_size:train_set_size + int(len(data) * test_ratio)]
    # 剩下的部分就是验证数据集
    dev_indices = shuffled_indices[train_set_size + int(len(data) * test_ratio):]
    # iloc选择参数序列中所对应的行
    return data.iloc[train_indices], data.iloc[test_indices], data.iloc[dev_indices]


# 使用sklearn库函数
def split_train_test_sklearn(data, test_ration=0.2, train_ration=0.8, random_state=42):
    if not isinstance(data, pandas.DataFrame):
        raise Exception('please use pandas read_csv read the file')
    return train_test_split(data, test_size=test_ration, train_size=train_ration, random_state=random_state)
