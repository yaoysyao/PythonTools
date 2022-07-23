# _*_ coding: utf-8 _*_
import inspect
import logging
import os.path
import re
import time
import sys
import colorlog

MY_LOG_INFO = logging.INFO
MY_LOG_ERROR = logging.ERROR
MY_LOG_DEBUG = logging.DEBUG
MY_LOG_WARN = logging.WARNING
MY_LOG_ALL = logging.DEBUG


class mylog(object):

    def __init__(self, log_name='log', log_path=None, log_level=None,
                 file_log_level=None, stream_log_level=None, save_log2_file=False, is_only_file=False):
        """
        :param logger:
               log_path：日志路径，默认为空，将保存至当前项目
               file_log_level：日志文件日志级别
               stream_log_level：控制台日志级别
               save_log2_file:是否需要保存至日志文件，默认是FALSE，如果为TRUE，则log_path不能为空
               log_level：日志级别，控制台会输出设置的级别及以上的日志，如设置info，会输出info级别和info级别以上的日志，这一点和日志文件的级别有本质的区别
        """
        self.__log_level = log_level
        self.__file_log_level = file_log_level
        self.__stream_log_level = stream_log_level
        self.__save_log2_file = save_log2_file
        self.__log_name = log_name
        # 设置日志路径
        self.__log_path = log_path

        # 只需要保存到文件，不需要在控制台输出,默认是FALSE
        self.is_only_file = is_only_file

        # 不同级别的日志颜色
        # 以下转义码可用于格式字符串：
        #
        # {color}, fg_{color}, bg_{color}: 前景色和背景色。
        # bold, bold_{color}, fg_bold_{color}, bg_bold_{color}: 粗体/明亮的颜色。
        # thin, thin_{color}, fg_thin_{color}: 淡色（取决于终端）。
        # reset：清除所有格式（前景色和背景色）。
        # 可用的颜色名称为black、red、green、yellow、blue、 purple和。cyanwhite
        # 如bg_white,白色背景
        self.__log_colors_config = {
            'DEBUG': 'white',  # cyan white
            'INFO': 'green,fg_bold_green',
            'WARNING': 'yellow,fg_bold_yellow',
            'ERROR': 'red,fg_bold_red',
            'CRITICAL': 'bold_red,fg_bold_bold_red',
        }

        if self.__save_log2_file is True or self.is_only_file is True:
            if self.__log_path is None:
                raise Exception('The save_log2_file or is_only_file is true,you must set a log path')

        # 日志一共分成5个等级，从高到低分别是：CRITICAL = FATAL > ERROR > WARNING =  WARN > INFO > DEBUG > NOTSET = 0
        # 保存日志时,会按照日志等级，保存该级别日志以及以下日志
        if self.__log_level is None:
            self.__log_level = MY_LOG_DEBUG
        if self.__file_log_level is None:
            self.__file_log_level = self.__log_level
        if self.__stream_log_level is None:
            self.__stream_log_level = self.__log_level

        # 创建一个logger
        self.__logger = logging.getLogger(self.__log_name)
        self.__logger.setLevel(self.__log_level)

        # 设置一些变量
        self.__all_log_name = None
        self.__info_log_name = None
        self.__error_log_name = None
        self.__debug_log_name = None
        self.__warn_log_name = None

        self.__all_file_handler = None
        self.__info_file_handler = None
        self.__error_file_handler = None
        self.__debug_file_handler = None
        self.__warn_file_handler = None
        self.__stream_handler = None

        # 设置formatter
        # __format_str = 'time:%(asctime)s -log_name:%(name)s -level:%(levelname)-s -file_name:%(filename)-8s -fun_name:%(funcName)s -chain:%(chain)s - %(lineno)d line -message: %(message)s'
        # -chain:%(chain)s:调用链路
        # - %(lineno)d line：行数,这种方法获取的行数为本文件中的写入日志的方法，并不是调用写日志的代码的行数，所以不用这种方法
        # self.__format_str = 'log_time:%(asctime)s -log_name:%(name)s -log_level:%(levelname)-s -log_filename:%(log_filename)s -func_name:%(func_name)s -line_number:%(line_number)d line -message: %(message)s'
        self.__format_str = '[%(asctime)s] [log_name:%(name)s] [%(levelname)s] [filename:%(log_filename)s] [func_name:%(func_name)s] [%(line_number)d line] -message:%(message)s'

        self.__formatter = logging.Formatter(self.__format_str)
        # 控制台日志输出格式，按照不同的颜色
        self.__console_formatter = colorlog.ColoredFormatter(
            # 格式
            fmt='%(log_color)s' + self.__format_str,
            # datefmt='%Y-%m-%d  %H:%M:%S',
            # 颜色
            log_colors=self.__log_colors_config
        )

        # 创建日志日期
        self.__log_day = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))

    def __set_stream_handler(self):
        # 再创建一个handler，用于输出到控制台
        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setLevel(self.__stream_log_level)
        # 控制台日志格式
        self.__stream_handler.setFormatter(self.__console_formatter)
        # 控制台handler
        if not (self.__stream_handler in self.__logger.handlers):
            self.__logger.addHandler(self.__stream_handler)

    def __remove_handler(self):
        pass

    def __set_log_file_name(self):
        # 如果不存在已经设置日志路径
        if self.__log_path is None:
            # os.getcwd()获取当前文件的路径，此时日志保存在当前工具类下log目录下，不建议不指定日志文件目录
            path_dir = os.path.dirname(__file__) + '/log' + '/' + self.__log_day
            # 如果该项目下没有log目录，创建log目录
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # os.path.dirname()获取指定文件路径的上级路径
            log_path = os.path.abspath(os.path.dirname(path_dir)) + '/log'
        else:
            # 否则，设置了路径就使用用户设置的路径
            path_dir = self.__log_path + '/' + self.__log_day
            # 最后为目录，不存在则创建
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

        # 创建日志名称。
        # rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 拼接日志文件路径名称
        self.__all_log_name = os.path.join(path_dir, self.__log_day + '-' + 'ALL' + '.log')
        self.__info_log_name = os.path.join(path_dir, self.__log_day + '-' + str(logging.getLevelName(MY_LOG_INFO)) + '.log')
        self.__error_log_name = os.path.join(path_dir, self.__log_day + '-' + str(logging.getLevelName(MY_LOG_ERROR)) + '.log')
        self.__debug_log_name = os.path.join(path_dir, self.__log_day + '-' + str(logging.getLevelName(MY_LOG_DEBUG)) + '.log')
        self.__warn_log_name = os.path.join(path_dir, self.__log_day + '-' + str(logging.getLevelName(MY_LOG_WARN)) + '.log')

    def __set_file_handler(self):
        # CRITICAL = FATAL > ERROR > WARNING =  WARN > INFO > DEBUG > NOTSET = 0
        # 创建一个通用的handler，用于写入日志文件，写入所有的日志级别
        self.__all_file_handler = logging.FileHandler(self.__all_log_name, encoding='utf-8')
        self.__all_file_handler.setLevel(self.__file_log_level)
        # 创建一个info_handler，用于写入INFO日志文件，只写入info级别及以下的日志
        self.__info_file_handler = logging.FileHandler(self.__info_log_name, encoding='utf-8')
        self.__info_file_handler.setLevel(MY_LOG_INFO)
        # 创建一个error_handler，用于写入ERROR日志文件，只写入error级别及以下的日志
        self.__error_file_handler = logging.FileHandler(self.__error_log_name, encoding='utf-8')
        self.__error_file_handler.setLevel(MY_LOG_ERROR)
        # 创建一个debug_handler，用于写入DEBUG日志文件，写入debug级别及以下的日志
        self.__debug_file_handler = logging.FileHandler(self.__debug_log_name, encoding='utf-8')
        self.__debug_file_handler.setLevel(MY_LOG_DEBUG)
        # 创建一个warn_handler，用于写入WARNING日志文件，写入WARNING级别及以下的日志
        self.__warn_file_handler = logging.FileHandler(self.__warn_log_name, encoding='utf-8')
        self.__warn_file_handler.setLevel(MY_LOG_WARN)

    def __set_file_formatter(self):
        # 日志文件日志格式
        self.__all_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        self.__info_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        self.__error_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        self.__debug_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        self.__warn_file_handler.setFormatter(self.__formatter)

    def __add_file_handler(self):
        # if not self.__logger.handlers:
        # 给logger添加handler
        # 如果保存到文件
        if not (self.__all_file_handler in self.__logger.handlers):
            # 所有日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__all_file_handler)

        if not (self.__info_file_handler in self.__logger.handlers):
            # info日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__info_file_handler)

        if not (self.__error_file_handler in self.__logger.handlers):
            # error日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__error_file_handler)

        if not (self.__debug_file_handler in self.__logger.handlers):
            # debug日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__debug_file_handler)

        if not (self.__warn_file_handler in self.__logger.handlers):
            # warning日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__warn_file_handler)

    def get_logger(self):
        if self.__save_log2_file is True or self.is_only_file is True:
            self.__set_log_file_name()
            self.__set_file_handler()
            self.__set_file_formatter()
            self.__add_file_handler()

        # 如果设置不输出控制台为FALSE
        if self.is_only_file is False:
            self.__set_stream_handler()
        # 日志重复输出，此设置不确定是否有效
        self.__logger.propagate = False
        return self.__logger

    @staticmethod
    def __get_file_name_in_full_path(file_path):
        return file_path.split('/')[-1]

    # 以下方法来源于https://github.com/frankyaorenjie/Python-CLog
    def get_meta_data(self):
        frames = inspect.stack()
        chain_list = []
        for i in range(0, len(frames)):
            _, file_path, _, func_name, _, _ = frames[i]
            file_name = self.__get_file_name_in_full_path(file_path)
            try:
                args = re.findall('\((.*)\)', frames[i + 1][-2][0])[0]
            except IndexError as e:
                func_result = self.__get_class_from_frame(frames[2][0])
                if func_result is None:
                    func_name = ''
                    args = ''
                else:
                    func_name = self.__get_class_from_frame(frames[2][0]).__name__
                    args = ''
            current_chain = '%s:%s(%s)' % (file_name, func_name, args)
            chain_list.append(current_chain)
        chain_list.reverse()
        return ' --> '.join(chain_list[-4:-2])

    @staticmethod
    def __get_class_from_frame(fr):
        args, _, _, value_dict = inspect.getargvalues(fr)
        if len(args) and args[0] == 'self':
            instance = value_dict.get('self', None)
            if instance:
                return getattr(instance, '__class__', None)
        return None


__self_my_log = None

__myLogger = None


def get_log(log_name='self_my_log', log_path=None, log_level=None, file_log_level=None,
            stream_log_level=None, save_log2_file=False, is_only_file=False):
    global __self_my_log
    __self_my_log = mylog(log_name=log_name, log_path=log_path, log_level=log_level, file_log_level=file_log_level,
                          stream_log_level=stream_log_level, save_log2_file=save_log2_file, is_only_file=is_only_file)
    return __self_my_log


def getLogger(log_name='self_my_log', log_path=None, log_level=None, file_log_level=None,
              stream_log_level=None, save_log2_file=False, is_only_file=False):
    global __self_my_log
    __self_my_log = get_log(log_name=log_name, log_path=log_path, log_level=log_level, file_log_level=file_log_level,
                            stream_log_level=stream_log_level, save_log2_file=save_log2_file, is_only_file=is_only_file)
    if __self_my_log is None:
        raise Exception('The global self_my_log is none,please set self_my_log')

    global __myLogger
    __myLogger = __self_my_log.get_logger()

    # 日志重复输出，此设置无效
    __myLogger.propagate = False
    return __myLogger


def get_chain():
    global __self_my_log
    if __self_my_log is None:
        return ''
    else:
        my_chain = mylog(log_name='self_my_log').get_meta_data()
        return my_chain


def _get_file_name():
    # 获取调用该方法的文件的名称。0指的是当前文件，1表示上一个文件，以栈的方式保存调用链路
    file_name = sys._getframe(2).f_code.co_filename
    if file_name != '' and file_name.count('/') >= 3:
        return '/'.join(str(i) for i in file_name.split('/')[-3:])
    else:
        return file_name


def _get_code_function_name():
    # 调用该函数的函数名字，如果没有被调用，则返回<module>
    function_name = sys._getframe(2).f_code.co_name
    if '<module>' in function_name:
        function_name = '非方法调用(Not function)'
    return function_name


def _get_code_line_number():
    # 调用该函数的函数名字，如果没有被调用，则返回<module>
    return sys._getframe(2).f_lineno


def log_info(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_INFO).get_logger()

    if my_logger.level != MY_LOG_INFO:
        my_logger.setLevel(MY_LOG_INFO)
    my_logger.info(message, extra={'chain': get_chain(), 'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # 暂时取消以下代码，因为如果不取消在demo中调用a方法，只能输出a中的日志，其他的方法中不输出，原因是因为，每次调用的时候handler被清空了，导致控制台handler没有了
    # my_logger.handlers = []


def log_error(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_ERROR).get_logger()

    if my_logger.level != MY_LOG_ERROR:
        my_logger.setLevel(MY_LOG_ERROR)
    my_logger.error(message, extra={'chain': get_chain(), 'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def log_warn(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_WARN).get_logger()

    if my_logger.level != MY_LOG_WARN:
        my_logger.setLevel(MY_LOG_WARN)
    my_logger.warning(message, extra={'chain': get_chain(), 'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def log_debug(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_DEBUG).get_logger()
    if my_logger.level != MY_LOG_DEBUG:
        my_logger.setLevel(MY_LOG_DEBUG)
    my_logger.debug(message, extra={'chain': get_chain(), 'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def get_log_level(my_logger=None):
    if my_logger is None:
        return -1
    else:
        return my_logger.level


# ==============================================demo=================================
# test_looger = getLogger(log_name='test')
#
#
# def a():
#     log_info('调用a方法', my_logger=test_looger)
#     b()
#
#
# def b():
#     log_info('调用b方法', my_logger=test_looger)
#     c()
#
#
# def c():
#     log_info('调用c方法', my_logger=test_looger)
#     d()
#
#
# def d():
#     log_info('调用d方法', my_logger=test_looger)
#     e()
#
#
# def e():
#     log_info('调用e方法', my_logger=test_looger)


if __name__ == '__main__':
    # a()
    test_looger = getLogger(log_name='test')
    log_info('log_infod')
    log_error('log_errora')
    log_debug('log_debugs')
    log_warn('log_warnd')

    log_info('1')
    log_error('2')
    log_debug('3')
    log_warn('4')

# error_log = mylog(logger='error').get_logger()

# error_log.error('错误日志测试')  #

# debug_log = mylog(logger='debug').get_logger()

# debug_log.debug('debug')
