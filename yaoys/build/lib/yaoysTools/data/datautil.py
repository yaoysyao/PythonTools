import numpy as np
from sklearn.model_selection import train_test_split


# 自定义划分测试数据集与训练数据集
def split_train_test(data, test_ratio=0.2):
    """
    :param
    data: 数据
    test_ratio:测试数据集的比例，默认0.2，按照2-8原则划分
    """
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


# 使用sklearn库函数
def split_train_test_sklearn(data, test_ration=0.2, train_ration=0.8, random_state=42):
    return train_test_split(data, test_size=test_ration, train_size=train_ration, random_state=random_state)
