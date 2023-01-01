# -*- coding: utf-8 -*-
# @FileName  :split_files.py
# @Time      :2022/10/24 21:39
# @Author    :yaoys
# @Desc      : 数据集按照一定的比例划分训练集和测试集
import csv
import os

from sklearn.model_selection import train_test_split


class SplitFiles(object):
    def __init__(self, **kwargs):
        """初始化"""
        # 要划分的数据集路径
        self.file_path = kwargs.get('file_path', None)
        # 训练数据集的比例
        self.train_size = kwargs.get('train_size', 0.8)
        # 测试数据集的比例
        self.test_size = kwargs.get('test_size', 1 - self.train_size)
        # 随机种子
        self.random_state = kwargs.get('random_state', 42)
        # 数据集数组
        self.data_list = []
        # 训练数据集数组
        self.train_data_list = []
        # 测试数据集数组
        self.test_data_list = []
        self.is_train = False
        self.is_test = False

        # 训练数据集保存地址
        self.train_data_path = kwargs.get('train_data_path', None)
        # 测试数据集保存地址
        self.test_data_path = kwargs.get('test_data_path', None)

        # self.logger = getLogger(log_name='SplitFiles', log_level=MY_LOG_INFO, save_log2_file=False)

        if self.file_path is None:
            raise Exception('The file_path is None')
        if self.train_data_path is None:
            raise Exception('The train_data_path is None')
        if self.test_data_path is None:
            raise Exception('The test_data_path is None')
        if self.train_size + self.test_size != 1:
            raise Exception('The train_size and test_size add must is 1')

    # 读取文件，并将文件的每一行保存在数组中
    def read_file(self):
        if os.path.exists(self.file_path) is False:
            raise Exception('The file path is error')

        with open(self.file_path, "r", encoding='utf-8') as data_file:
            for line in data_file:
                self.data_list.append(line.strip())

    # 按照比例划分数据
    def splitFile(self):

        # 文件格式只能是csv或者TXT
        if os.path.splitext(self.train_data_path)[1] not in ['.csv'] and os.path.splitext(self.test_data_path)[1] not in ['.csv'] \
                and os.path.splitext(self.train_data_path)[1] not in ['.txt'] and os.path.splitext(self.test_data_path)[1] not in ['.txt']:
            raise Exception('The file type must csv or txt')
        # log_info('load data.....', my_logger=self.logger)
        # 读取所有的数据
        self.read_file()
        # log_info('split data', my_logger=self.logger)
        # 使用sklearn划分训练数据集和测试数据集
        self.train_data_list, self.test_data_list = train_test_split(self.data_list, test_size=self.test_size, train_size=self.train_size, random_state=self.random_state)
        # 保存文件
        # log_info('save train data and test data.....', my_logger=self.logger)
        self.save_result()

    # 保存划分好的数据集
    def save_result(self):
        try:
            # 该方法返回两个元素, 第一个是路径去掉后缀的部分, 第二个是文件后缀
            # 如果是Excel文件
            if os.path.splitext(self.train_data_path)[1] in ['.csv']:
                self.is_train = True
                self.is_test = False
                self.save_excel_result()
            if os.path.splitext(self.test_data_path)[1] in ['.csv']:
                self.is_train = False
                self.is_test = True
                self.save_excel_result()
            #     txt文件
            if os.path.splitext(self.train_data_path)[1] in ['.txt']:
                self.is_train = True
                self.is_test = False
                self.save_txt_result()
            if os.path.splitext(self.test_data_path)[1] in ['.txt']:
                self.is_train = False
                self.is_test = True
                self.save_txt_result()

        except:
            print('error')

    def save_txt_result(self):
        train_file = None
        test_file = None
        try:
            if self.is_train is True and self.is_test is False:
                self.exists_and_remove_file()
                # log_info('save train txt data.....', my_logger=self.logger)
                train_file = open(self.train_data_path, 'a', encoding='utf-8')

                for i in range(0, len(self.train_data_list)):
                    train_file.write(self.train_data_list[i] + '\n')

                train_file.close()

            if self.is_train is False and self.is_test is True:
                self.exists_and_remove_file()
                # log_info('save train txt data.....', my_logger=self.logger)
                test_file = open(self.test_data_path, 'a', encoding='utf-8')

                for i in range(0, len(self.test_data_list)):
                    test_file.write(self.test_data_list[i] + '\n')

                test_file.close()

        except:
            if train_file is not None:
                train_file.close()
            if test_file is not None:
                test_file.close()
            print('')

        self.is_train = False
        self.is_test = False

    def save_excel_result(self):
        if self.is_train is True and self.is_test is False:
            self.exists_and_remove_file()
            # log_info('save train excel data.....', my_logger=self.logger)
            f = open(self.train_data_path, 'a', encoding='utf-8', newline='')
            # 2. 基于文件对象构建 csv写入对象
            csv_writer = csv.writer(f)

            for i in range(0, len(self.train_data_list)):
                data_row = self.train_data_list[i]
                row = []
                for j in range(0, len(data_row.split(','))):
                    row.append(data_row.split(',')[j])
                csv_writer.writerow(row)

            f.close()
        if self.is_train is False and self.is_test is True:
            self.exists_and_remove_file()
            # log_info('save test excel data.....', my_logger=self.logger)
            f = open(self.test_data_path, 'a', encoding='utf-8', newline='')
            # 2. 基于文件对象构建 csv写入对象
            csv_writer = csv.writer(f)

            for i in range(0, len(self.test_data_list)):
                data_row = self.test_data_list[i]
                row = []
                for j in range(0, len(data_row.split(','))):
                    row.append(data_row.split(',')[j])
                csv_writer.writerow(row)
            f.close()
        self.is_train = False
        self.is_test = False

    def exists_and_remove_file(self):
        if self.is_train is True and self.is_test is False:
            if os.path.exists(self.train_data_path):
                # log_info('exists train file and remove the file', my_logger=self.logger)
                os.remove(self.train_data_path)

        if self.is_train is False and self.is_test is True:
            if os.path.exists(self.test_data_path):
                # log_info('exists test file and remove the file', my_logger=self.logger)
                os.remove(self.test_data_path)
