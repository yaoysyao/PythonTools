# -*- coding: utf-8 -*-
# @FileName  :file_util_demo.py
# @Time      :2023/1/2 17:10
# @Author    :yaoys
# @Desc      :
from yaoysTools.file.file_util import *

list = ['a  c', 'd   b', 12]
# to TXT
to_txt(list, file_path='../demoFile/file_util.txt')

# read TXT
print(read_txt(file_path='../demoFile/file_util.txt', read_model='read_line', line_count=0))

# read csv
data = read_csv(file_path='../demoFile/data_test.csv')
print(data)

# to csv
to_csv(data, file_path='../demoFile/file_until.csv')
