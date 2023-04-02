import time

from yaoysTools.log.logutil import MY_LOG_ALL, MY_LOG_DEBUG, MY_LOG_ERROR, MY_LOG_INFO, getLogger, log_debug, log_error, log_info, log_warn

for i in range(0, 3):
    test_looger = getLogger(log_name='test',
                            save_log2_file=True,
                            log_path='../../demo/log',
                            is_only_file=False,
                            log_level=MY_LOG_INFO,
                            file_log_level=MY_LOG_DEBUG,
                            stream_log_level=MY_LOG_ERROR,
                            is_split_log=False,
                            is_all_file=False,
                            log_file_name='test',
                            is_color_console=False
                            )
    log_info('log_info' + str(i), my_logger=test_looger)
    log_error('log_error' + str(i), my_logger=test_looger)
    log_debug('log_debug' + str(i), my_logger=test_looger)
    log_warn('log_warn' + str(i), my_logger=test_looger)
    print('==============================================')
    time.sleep(1)

    test_looger = getLogger(log_name='test1111',
                            save_log2_file=True,
                            log_path='../../demo/log',
                            is_only_file=False,
                            log_level=MY_LOG_INFO,
                            file_log_level=MY_LOG_DEBUG,
                            stream_log_level=MY_LOG_DEBUG,
                            is_split_log=False,
                            is_all_file=False,
                            log_file_name='test111',
                            is_color_console=True
                            )
    log_info('log_info' + str(i), my_logger=test_looger)
    log_error('log_error' + str(i), my_logger=test_looger)
    log_debug('log_debug' + str(i), my_logger=test_looger)
    log_warn('log_warn' + str(i), my_logger=test_looger)
    print('==============================================')
    time.sleep(1)
