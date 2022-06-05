# _*_ coding: utf-8 _*_
import logging
import os.path
import time


class mylog(object):

    def __init__(self, logger='log', log_path=None, log_level=None, file_log_level=None, stream_log_level=None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
               log_path：日志路径，默认为空，将保存至当前项目
               file_log_level：日志文件日志级别
               stream_log_level：控制台日志级别
        """
        self.log_level = log_level
        self.file_log_level = file_log_level
        self.stream_log_level = stream_log_level

        # 初始化，不指定日志级别，默认为Debug,此时，会打印出debug级别及以上的全部日志，并保存至日期-debug文件中
        '''
        日志一共分成5个等级，从低到高分别是：
            DEBUG
            INFO
            WARNING
            ERROR
            CRITICAL
        '''
        if self.log_level is None:
            self.log_level = logging.DEBUG
        if self.file_log_level is None:
            self.file_log_level = self.log_level
        if self.stream_log_level is None:
            self.stream_log_level = self.log_level

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(self.log_level)
        # 设置日志路径
        self.log_path = log_path

        # 创建日志名称。
        rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        # 如果不存在已经设置日志路径
        if self.log_path is None:
            # os.getcwd()获取当前文件的路径，
            path_dir = os.path.dirname(__file__) + '/log'
            # 如果该项目下没有log目录，创建log目录
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # os.path.dirname()获取指定文件路径的上级路径
            log_path = os.path.abspath(os.path.dirname(path_dir)) + '/log'
        else:
            # 否则，设置了路径就使用用户设置的路径
            path_dir = self.log_path

        # 拼接日志文件路径名称
        log_name = os.path.join(path_dir, rq + '-' + 'ALL' + '.log')
        info_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.INFO)) + '.log')
        error_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.ERROR)) + '.log')
        debug_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.DEBUG)) + '.log')

        # 创建一个通用的handler，用于写入日志文件，写入所有的日志级别
        fh = logging.FileHandler(log_name, encoding='utf-8')
        fh.setLevel(self.file_log_level)
        # 创建一个info_handler，用于写入INFO日志文件，只写入info级别及以上的日志
        info_fh = logging.FileHandler(info_log_name, encoding='utf-8')
        info_fh.setLevel(logging.INFO)
        # 创建一个error_handler，用于写入ERROR日志文件，只写入error级别及以上的日志
        error_fh = logging.FileHandler(error_log_name, encoding='utf-8')
        error_fh.setLevel(logging.ERROR)
        # 创建一个debug_handler，用于写入DEBUG日志文件，写入debug级别及以上的日志
        debug_fh = logging.FileHandler(debug_log_name, encoding='utf-8')
        debug_fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.stream_log_level)

        # 定义handler的输出格式  #日志输出的格式
        '''
        logging.basicConfig函数中，可以指定日志的输出格式format，这个参数可以输出很多有用的信息，如下:
            %(levelno)s: 打印日志级别的数值
            %(levelname)s: 打印日志级别名称
            %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
            %(filename)s: 打印当前执行程序名
            %(funcName)s: 打印日志的当前函数,如果在main方法调用，会输出<moudle>
            %(lineno)d: 打印日志的当前行号
            %(asctime)s: 打印日志的时间
            %(thread)d: 打印线程ID
            %(threadName)s: 打印线程名称
            %(process)d: 打印进程ID
            %(message)s: 打印日志信息
        '''
        format_str = 'time:%(asctime)s -log_name:%(name)s -level:%(levelname)-s -file_name:%(filename)-8s -fun_name:%(funcName)s - %(lineno)d line -message: %(message)s'
        formatter = logging.Formatter(format_str)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        info_fh.setFormatter(formatter)
        error_fh.setFormatter(formatter)
        debug_fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.addHandler(info_fh)
        self.logger.addHandler(error_fh)
        self.logger.addHandler(debug_fh)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6]
    info_log = mylog(logger='[Demo]').get_logger()
    info_log.info('测试日志')
    info_log.error('error 测试日志')
    info_log.debug('debug 测试日志')

    # error_log = mylog(logger='error').get_logger()

    # error_log.error('错误日志测试')  #

    # debug_log = mylog(logger='debug').get_logger()

    # debug_log.debug('debug')
