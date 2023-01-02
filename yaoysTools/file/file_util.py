# -*- coding: utf-8 -*-
# @FileName  :file_util.py
# @Time      :2023/1/2 15:57
# @Author    :yaoys
# @Desc      :文件工具类，读取文件，写入文件等
import os
from typing import List, Optional, Union

import pandas as pd


# 使用pandas读取csv文件
def read_csv(file_path: Union[str] = None, encoding='UTF-8', need2_dataframe=False):
    if file_path is None:
        raise Exception('the file is not exist')

    data = pd.read_csv(filepath_or_buffer=file_path, encoding=encoding)
    if need2_dataframe:
        data = pd.DataFrame(data=data)
    return data


# 写入csv文件
def to_csv(data: Union[pd.DataFrame] = None, file_path=None, encoding='UTF-8', index=False, header: Union[bool, List[str]] = True, sep=','):
    '''

    :param data: 要写入的数据,格式为使用pandas读取的数据
    :param file_path: 文件路径
    :param encoding: 编码格式
    :param index: 是否写入索引，默认是FALSE
    :param header: 是否保留列名，默认为TRUE，为TRUE则使用pandas读取的数据的列名不做其他修改，如果为list，则设置新列名
    :param sep: 分隔字符
    :return:
    '''
    if file_path is None:
        raise Exception('if save file,the file_path is required')

    if data is None:
        raise Exception('if save file,the data is required')

    data.to_csv(path_or_buf=file_path, index=index, encoding=encoding, sep=sep, header=header)


# 读取TXT文件，读取模式为按行读取所有，读取某一行,默认为按行读取所有，返回为一个list,如果读取某一行，需要设置line_count参数
def read_txt(file_path: Union[str] = None, encoding='UTF-8', read_model: Union[str] = 'all', line_count: Union[int] = -1):
    '''
    :param file_path:
    :param encoding:
    :param read_model: all(read all) or read_line(read one line)
    :param line_count: 读取的行数
    :return:
    '''
    result = []

    if os.path.exists(file_path) is False:
        raise Exception('The file path is error')

    if read_model == 'all':
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f.readlines():
                # 去除文本中的换行符
                line = line.strip('\n')
                result.append(line)
    elif read_model == 'read_line':
        if line_count < 0:
            raise Exception('If you want to read line, you must set line_count >=0')

        count = 0

        with open(file_path, 'r', encoding=encoding) as f:
            if line_count > len(f.readlines()):
                raise Exception('The number of rows read is greater than the total number of rows')

        with open(file_path, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line_count == count:
                    # 去除文本中的换行符
                    line = line.strip('\n')
                    result.append(line)
                    break
                count = count + 1

    return result


def to_txt(data: Optional[List] = None, file_path: Union[str] = None, encoding='UTF-8'):
    '''

    :param data: 要写入的数据，格式为list
    :param file_path: 文件路径
    :param encoding: 编码
    :return:
    '''
    if data is None:
        raise Exception('The data is None')

    if isinstance(data, list) is False:
        raise Exception('The data must is list')

    if file_path is None:
        raise Exception('The file path is error')
    f = open(file_path, 'w', encoding=encoding)
    # into txt
    for line in data:
        f.writelines(str(line) + '\n')
    f.close()
