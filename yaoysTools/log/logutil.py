# _*_ coding: utf-8 _*_
import inspect
import logging
import os.path
import sys
import time

import colorlog

MY_LOG_INFO = logging.INFO
MY_LOG_ERROR = logging.ERROR
MY_LOG_DEBUG = logging.DEBUG
MY_LOG_WARN = logging.WARNING
MY_LOG_ALL = logging.DEBUG


# 解决日志重复输出的问题，参考自：https://github.com/ydf0509/nb_log
def my_addHandler(self, hdlr):
    """
    Add the specified handler to this logger.
    """
    logging._acquireLock()  # noqa

    try:
        """ 官方代码
        if not (hdlr in self.handlers):
            self.handlers.append(hdlr)
        """
        # 解决的原理就是，每次需要新增时，判断原有的handler中是否存在相同的日志级别的handler，如果存在相同的，则加入到set中，此时不加入handlers
        hdlrx_set = set()
        for hdlrx in self.handlers:
            hdlrx_type = type(hdlrx)
            if hdlrx.level == hdlr.level:
                hdlrx_set.add(hdlrx_type)

        hdlr_type = type(hdlr)
        if hdlr_type not in hdlrx_set:
            self.handlers.append(hdlr)
    finally:
        logging._releaseLock()


# 重写logging模块的addHandler方法，实现同一个logger不重复添加相同的handler，解决重复打印和重复写入文件的问题
logging.Logger.addHandler = my_addHandler


class mylog(object):

    def __init__(self, **kwargs):
        """
        :param
               log_name：日志名称
               log_path：日志路径，若save_log2_file=True，则该参数不能为空
               log_level：日志级别，如果file_log_level和stream_log_level为None，则默认使用log_level级别，如果log_level也为None，则三者同时默认级别为Info级别
               使用控制台会输出设置的级别及以上的日志，如设置info，会输出info级别和info级别以上的日志，这一点和日志文件的级别有本质的区别
               file_log_level：日志文件日志级别
               stream_log_level：控制台日志级别
               save_log2_file:是否需要保存至日志文件，默认是FALSE，如果为TRUE，则log_path不能为空
               is_only_file:日志只保存至日志文件，不在控制台输出，该参数主要用在进度条模块中，设置进度条保存在日志文件中时，需要设置该参数为True，保证不在控制台输出日志进度而保存到文件
               is_split_log:是否按照日期分割日志文件，默认为False，如果设置为True，则会按照每天的日期产生文件夹和日志文件
               is_all_file:生成日志文件时是否产生全部日志文件，默认为False，此时只产生一个日志文件，设置为True，则会产生不同级别的日志文件
               log_file_name:日志文件名称，默认为log
               is_color_console:控制台输出是否区分颜色，默认为FALSE
        """

        self.__log_level = kwargs.get('log_level', MY_LOG_INFO)
        self.__file_log_level = kwargs.get('file_log_level', None)
        self.__stream_log_level = kwargs.get('stream_log_level', None)
        self.__save_log2_file = kwargs.get('save_log2_file', False)
        self.__log_name = kwargs.get('log_name', 'log')
        self.__is_split_log = kwargs.get('is_split_log', False)
        self.__is_all_file = kwargs.get('is_all_file', False)
        self.__log_file_name = kwargs.get('log_file_name', 'log')
        self.__is_color_console = kwargs.get('is_color_console', False)
        # 设置日志路径
        self.__log_path = kwargs.get('log_path', None)

        # 只需要保存到文件，不需要在控制台输出,默认是FALSE
        self.is_only_file = kwargs.get('is_only_file', False)

        if self.__save_log2_file is True or self.is_only_file is True:
            if self.__log_path is None:
                raise Exception('The save_log2_file or is_only_file is true,you must set a log path')

        # 日志一共分成5个等级，从高到低分别是：CRITICAL = FATAL > ERROR > WARNING =  WARN > INFO > DEBUG > NOTSET = 0
        # 保存日志时,会按照日志等级，保存该级别日志以及以上日志
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
        self.__one_log_name = None
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
        self.__one_file_handler = None

        # 设置formatter
        # __format_str = 'time:%(asctime)s -log_name:%(name)s -level:%(levelname)-s -file_name:%(filename)-8s -fun_name:%(funcName)s -chain:%(chain)s - %(lineno)d line -message: %(message)s'
        # -chain:%(chain)s:调用链路
        # - %(lineno)d line：行数,这种方法获取的行数为本文件中的写入日志的方法，并不是调用写日志的代码的行数，所以不用这种方法
        # self.__format_str = 'log_time:%(asctime)s -log_name:%(name)s -log_level:%(levelname)-s -log_filename:%(log_filename)s -func_name:%(func_name)s -line_number:%(line_number)d line -message: %(message)s'
        self.__format_str = kwargs.get('format_str', '[%(asctime)s][%(name)s][%(levelname)s][%(log_filename)s][%(line_number)d line] message:%(message)s')

        self.__formatter = logging.Formatter(self.__format_str)
        # 控制台日志输出格式，按照不同的颜色
        # 不同级别的日志颜色
        # 以下转义码可用于格式字符串：
        #
        # {color}, fg_{color}, bg_{color}: 前景色和背景色。
        # bold, bold_{color}, fg_bold_{color}, bg_bold_{color}: 粗体/明亮的颜色。
        # thin, thin_{color}, fg_thin_{color}: 淡色（取决于终端）。
        # reset：清除所有格式（前景色和背景色）。
        # 可用的颜色名称为black、red、green、yellow、blue、 purple和。cyanwhite
        # 如bg_white,白色背景
        self.__log_colors_config = kwargs.get('log_colors_config', {
            'DEBUG': 'white',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red,fg_bold_bold_red',
        })
        self.__console_color_formatter = colorlog.ColoredFormatter(
            # 格式
            fmt='%(log_color)s' + self.__format_str,
            # datefmt='%Y-%m-%d  %H:%M:%S',
            # 颜色
            log_colors=self.__log_colors_config,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 创建日志日期
        self.__log_day = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))

    def __set_stream_handler(self):
        # 再创建一个handler，用于输出到控制台
        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setLevel(self.__stream_log_level)
        # 控制台日志格式
        if self.__is_color_console is True:
            self.__stream_handler.setFormatter(self.__console_color_formatter)
        else:
            self.__stream_handler.setFormatter(self.__formatter)
        # 控制台handler
        if not (self.__stream_handler in self.__logger.handlers):
            self.__logger.addHandler(self.__stream_handler)

    def __remove_handler(self):
        pass

    def __set_log_file_name(self):
        # 如果不存在已经设置日志路径
        if self.__log_path is None:
            # os.getcwd()获取当前文件的路径，此时日志保存在当前工具类下log目录下，不建议不指定日志文件目录
            path_dir = os.path.dirname(__file__) + '/log'
            if self.__is_split_log is True:
                path_dir = path_dir + '/' + self.__log_day
            # 如果该项目下没有log目录，创建log目录
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # os.path.dirname()获取指定文件路径的上级路径
            # log_path = os.path.abspath(os.path.dirname(path_dir)) + '/log'
        else:
            # 否则，设置了路径就使用用户设置的路径
            path_dir = self.__log_path
            if self.__is_split_log is True:
                path_dir = path_dir + '/' + self.__log_day
            # 最后为目录，不存在则创建
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

        # 创建日志名称。
        # rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 拼接日志文件路径名称
        # 如果需要生成全部日志文件并且需要按照日期分割
        if self.__is_all_file is True and self.__is_split_log is True:
            self.__all_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '_' + 'all' + '.log')
            self.__info_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_INFO)).lower() + '.log')
            self.__error_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_ERROR)).lower() + '.log')
            self.__debug_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_DEBUG)).lower() + '.log')
            self.__warn_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_WARN)).lower() + '.log')
        #     如果需要生成全部日志文件，但是不按照日期分割
        elif self.__is_all_file is True and self.__is_split_log is False:
            self.__all_log_name = os.path.join(path_dir, self.__log_file_name + '_' + 'all' + '.log')
            self.__info_log_name = os.path.join(path_dir, self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_INFO)).lower() + '.log')
            self.__error_log_name = os.path.join(path_dir, self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_ERROR)).lower() + '.log')
            self.__debug_log_name = os.path.join(path_dir, self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_DEBUG)).lower() + '.log')
            self.__warn_log_name = os.path.join(path_dir, self.__log_file_name + '_' + str(logging.getLevelName(MY_LOG_WARN)).lower() + '.log')
        #     如果不需要生成全部日志文件，但是需要按照日期分割,此时只需要生成设置的日志级别的日志文件即可
        elif self.__is_all_file is False and self.__is_split_log is True:
            if self.__log_level == MY_LOG_INFO:
                self.__info_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '.log')
            elif self.__log_level == MY_LOG_ERROR:
                self.__error_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '.log')
            elif self.__log_level == MY_LOG_DEBUG:
                self.__debug_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '.log')
            elif self.__log_level == MY_LOG_WARN:
                self.__warn_log_name = os.path.join(path_dir, self.__log_day + '_' + self.__log_file_name + '.log')
            else:
                raise Exception('Thr log level is not in [info,warn,error,debug]')
        # 如果既不需要生成所有的日志文件，也不需要按照日期分割，那么则只需要按照当前日志级别生成一个名称不带日期的日志文件
        elif self.__is_all_file is False and self.__is_split_log is False:
            self.__one_log_name = os.path.join(path_dir, self.__log_file_name + '.log')
        else:
            raise Exception('The is_all_file or is_split_log args error!')

    def __set_file_handler(self):
        # CRITICAL = FATAL > ERROR > WARNING =  WARN > INFO > DEBUG > NOTSET = 0
        # 创建一个通用的handler，用于写入日志文件，写入所有的日志级别
        # if self.__all_log_name is not None:
        #     self.__all_file_handler = logging.FileHandler(self.__all_log_name, encoding='utf-8')
        #     self.__all_file_handler.setLevel(self.__file_log_level)
        # 创建一个info_handler，用于写入INFO日志文件，只写入info级别以上的日志
        if self.__info_log_name is not None:
            self.__info_file_handler = logging.FileHandler(self.__info_log_name, encoding='utf-8')
            self.__info_file_handler.setLevel(MY_LOG_INFO)
        # 创建一个error_handler，用于写入ERROR日志文件，只写入error级别以上的日志
        if self.__error_log_name is not None:
            self.__error_file_handler = logging.FileHandler(self.__error_log_name, encoding='utf-8')
            self.__error_file_handler.setLevel(MY_LOG_ERROR)
        # 创建一个debug_handler，用于写入DEBUG日志文件，写入debug级别以上的日志
        if self.__debug_log_name is not None:
            self.__debug_file_handler = logging.FileHandler(self.__debug_log_name, encoding='utf-8')
            self.__debug_file_handler.setLevel(MY_LOG_DEBUG)
        # 创建一个warn_handler，用于写入WARNING日志文件，写入WARNING级别以上的日志
        if self.__warn_log_name is not None:
            self.__warn_file_handler = logging.FileHandler(self.__warn_log_name, encoding='utf-8')
            self.__warn_file_handler.setLevel(MY_LOG_WARN)
        #     创建一个one_handler，用于写入log_level日志文件
        if self.__one_log_name is not None:
            self.__one_file_handler = logging.FileHandler(self.__one_log_name, encoding='utf-8')
            self.__one_file_handler.setLevel(self.__file_log_level)

    def __set_file_formatter(self):
        # 日志文件日志格式
        # if self.__all_file_handler is not None:
        #     self.__all_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        if self.__info_file_handler is not None:
            self.__info_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        if self.__error_file_handler is not None:
            self.__error_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        if self.__debug_file_handler is not None:
            self.__debug_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        if self.__warn_file_handler is not None:
            self.__warn_file_handler.setFormatter(self.__formatter)
        # 日志文件日志格式
        if self.__one_file_handler is not None:
            self.__one_file_handler.setFormatter(self.__formatter)

    def __add_file_handler(self):
        # if not self.__logger.handlers:
        # 给logger添加handler
        # 如果保存到文件
        # if not (self.__all_file_handler in self.__logger.handlers) and self.__all_file_handler is not None:
        #     # 所有日志级别handler，如果不配置，则无法写入文件
        #     self.__logger.addHandler(self.__all_file_handler)

        # 如果handler不是None,并且不在handlers中，并且设置的文本日志级别小于或者等于info级别，此时将设置info，日志文件中写入大于等于info级别的日志
        if not (self.__info_file_handler in self.__logger.handlers) and self.__info_file_handler is not None and self.__file_log_level <= MY_LOG_INFO:
            # info日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__info_file_handler)

        if not (self.__error_file_handler in self.__logger.handlers) and self.__error_file_handler is not None and self.__file_log_level <= MY_LOG_ERROR:
            # error日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__error_file_handler)

        if not (self.__debug_file_handler in self.__logger.handlers) and self.__debug_file_handler is not None and self.__file_log_level <= MY_LOG_DEBUG:
            # debug日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__debug_file_handler)

        if not (self.__warn_file_handler in self.__logger.handlers) and self.__warn_file_handler is not None and self.__file_log_level <= MY_LOG_WARN:
            # warning日志级别handler，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__warn_file_handler)

        if not (self.__one_file_handler in self.__logger.handlers) and self.__one_file_handler is not None:
            # 不按照日期分割和不需要生成所有日志文件，如果不配置，则无法写入文件
            self.__logger.addHandler(self.__one_file_handler)

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
    # def get_meta_data(self):
    #     frames = inspect.stack()
    #     chain_list = []
    #     for i in range(0, len(frames)):
    #         _, file_path, _, func_name, _, _ = frames[i]
    #         file_name = self.__get_file_name_in_full_path(file_path)
    #         try:
    #             args = re.findall('\((.*)\)', frames[i + 1][-2][0])[0]
    #         except IndexError as e:
    #             func_result = self.__get_class_from_frame(frames[2][0])
    #             if func_result is None:
    #                 func_name = ''
    #                 args = ''
    #             else:
    #                 func_name = self.__get_class_from_frame(frames[2][0]).__name__
    #                 args = ''
    #         current_chain = '%s:%s(%s)' % (file_name, func_name, args)
    #         chain_list.append(current_chain)
    #     chain_list.reverse()
    #     return ' --> '.join(chain_list[-4:-2])

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


def get_log(log_name='self_my_log',
            log_path=None,
            log_level=None,
            file_log_level=None,
            stream_log_level=None,
            save_log2_file=False,
            is_only_file=False,
            is_split_log=False,
            is_all_file=False,
            log_file_name='log',
            is_color_console=False):
    global __self_my_log
    __self_my_log = mylog(log_name=log_name,
                          log_path=log_path,
                          log_level=log_level,
                          file_log_level=file_log_level,
                          stream_log_level=stream_log_level,
                          save_log2_file=save_log2_file,
                          is_only_file=is_only_file,
                          is_split_log=is_split_log,
                          is_all_file=is_all_file,
                          log_file_name=log_file_name,
                          is_color_console=is_color_console)
    return __self_my_log


def getLogger(log_name='self_my_log',
              log_path=None,
              log_level=None,
              file_log_level=None,
              stream_log_level=None,
              save_log2_file=False,
              is_only_file=False,
              is_split_log=False,
              is_all_file=False,
              log_file_name='log',
              is_color_console=False):
    global __self_my_log
    __self_my_log = get_log(log_name=log_name,
                            log_path=log_path,
                            log_level=log_level,
                            file_log_level=file_log_level,
                            stream_log_level=stream_log_level,
                            save_log2_file=save_log2_file,
                            is_only_file=is_only_file,
                            is_split_log=is_split_log,
                            is_all_file=is_all_file,
                            log_file_name=log_file_name,
                            is_color_console=is_color_console)
    if __self_my_log is None:
        raise Exception('The global self_my_log is none,please set self_my_log')

    global __myLogger
    __myLogger = __self_my_log.get_logger()

    # 日志重复输出，此设置无效
    __myLogger.propagate = False
    return __myLogger


# def get_chain():
#     global __self_my_log
#     if __self_my_log is None:
#         return ''
#     else:
#         my_chain = mylog(log_name='self_my_log').get_meta_data()
#         return my_chain


def _get_file_name():
    # 获取调用该方法的文件的名称。0指的是当前文件，1表示上一个文件，以栈的方式保存调用链路
    file_name = sys._getframe(2).f_code.co_filename
    if file_name != '' and file_name.count('/') >= 1:
        return '/'.join(str(i) for i in file_name.split('/')[-1:])
    elif file_name != '' and file_name.count('\\') >= 1:
        return '\\'.join(str(i) for i in file_name.split('\\')[-1:])
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


# 'chain': get_chain() 输出调用链路，无实际作用
def log_info(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_INFO).get_logger()

    if my_logger.level != MY_LOG_INFO:
        my_logger.setLevel(MY_LOG_INFO)
    my_logger.info(message, extra={'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # 暂时取消以下代码，因为如果不取消在demo中调用a方法，只能输出a中的日志，其他的方法中不输出，原因是因为，每次调用的时候handler被清空了，导致控制台handler没有了
    # my_logger.handlers = []


def log_error(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_ERROR).get_logger()

    if my_logger.level != MY_LOG_ERROR:
        my_logger.setLevel(MY_LOG_ERROR)
    my_logger.error(message, extra={'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def log_warn(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_WARN).get_logger()

    if my_logger.level != MY_LOG_WARN:
        my_logger.setLevel(MY_LOG_WARN)
    my_logger.warning(message, extra={'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def log_debug(message, my_logger=None):
    if my_logger is None and __myLogger is not None:
        my_logger = __myLogger
    if my_logger is None and __myLogger is None:
        my_logger = get_log(log_level=MY_LOG_DEBUG).get_logger()
    if my_logger.level != MY_LOG_DEBUG:
        my_logger.setLevel(MY_LOG_DEBUG)
    # '''chain': get_chain(),'''
    my_logger.debug(message, extra={'log_filename': _get_file_name(), 'func_name': _get_code_function_name(), 'line_number': _get_code_line_number()})
    # my_logger.handlers = []


def get_log_level(my_logger=None):
    if my_logger is None:
        return -1
    else:
        return my_logger.level
