import sys

from yaoysTools.log.logutil import getLogger
from yaoysTools.log.logutil import log_info
from yaoysTools.log.logutil import MY_LOG_INFO

# 打包上传命令:PS E:\MyJob\PyCharm\PythonTools\yaoys> python setup.py sdist,注意目录
# twine upload dist/yaoys-python-tool-0.0.30.tar.gz


# logger = getLogger(log_name='testMain', save_log2_file=True, log_level=MY_LOG_INFO, log_path='./demo/log')
# log_info('test', my_logger=logger)
#
# print(sys._getframe().f_code.co_filename)
# print(sys._getframe(1).f_code.co_filename)
# print(sys._getframe(0).f_code.co_name)  # 当前函数名
# print(sys._getframe(1).f_code.co_name)  # 调用该函数的函数名字，如果没有被调用，则返回<module>
# print(sys._getframe(0).f_lineno)  # 当前函数的行号
# print(sys._getframe(1).f_lineno)  # 调用该函数的行号
#
# t = 'E:/MyJob/PyCharm/PyFakeReview/fake_review/main.py'
# print(t.split('/')[-3:])
# print('/'.join(str(i) for i in t.split('/')[-3:]))


test_looger = getLogger(log_name='test')


def a():
    log_info('调用a方法', my_logger=test_looger)
    b()


def b():
    log_info('调用b方法', my_logger=test_looger)
    c()


def c():
    log_info('调用c方法', my_logger=test_looger)
    d()


def d():
    log_info('调用d方法', my_logger=test_looger)
    e()


def e():
    log_info('调用e方法', my_logger=test_looger)


if __name__ == '__main__':
    a()
