# _*_ coding: utf-8 _*_
import logging
import os.path
import time


class logUtil(object):

    def __init__(self, logger='log', logpath=None, loggerlevel=logging.DEBUG, fileloggerlevel=logging.INFO, streamloggerlevel=logging.INFO):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
               logpath：日志路径，默认为空，将保存至当前项目
               fileloggerlevel：日志文件日志级别
               streamloggerlevel：控制台日志级别
        """
        self.loggerlevel = loggerlevel
        self.fileloggerlevel = fileloggerlevel
        self.streamloggerlevel = streamloggerlevel
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(loggerlevel)
        # 设置日志路径
        self.logpath = logpath

        # 创建日志名称。
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))

        # 如果不存在已经设置日志路径
        if self.logpath is None:
            # os.getcwd()获取当前文件的路径，
            path_dir = os.path.dirname(__file__) + '/log'
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # os.path.dirname()获取指定文件路径的上级路径
            log_path = os.path.abspath(os.path.dirname(path_dir)) + '/log'
        else:  # 否则，设置了路径就使用用户设置的路径
            path_dir = self.logpath

        log_name = os.path.join(path_dir, rq + '.' + str(logging.getLevelName(fileloggerlevel)) + '.log')

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name, encoding='utf-8')
        fh.setLevel(self.fileloggerlevel)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.streamloggerlevel)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def log_info(self, message=None, *args):
        self.get_logger().info(message, args)

    def log_error(self, message=None, *args):
        self.get_logger().error(message, args)


if __name__ == '__main__':
    log = logUtil(logger='[Demo]', logpath='E:\\log\\pythonTool').get_logger()
    log.error('测试日志')
