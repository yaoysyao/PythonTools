from yaoysTools.log.logutil import MY_LOG_ALL, MY_LOG_DEBUG, MY_LOG_INFO, getLogger, log_debug, log_error, log_info, log_warn

test_looger = getLogger(log_name='test', save_log2_file=True, log_path='../../demo/log', is_only_file=False, log_level=MY_LOG_ALL, is_split_log=False, is_all_file=True, log_file_name='test')
log_info('log_info', my_logger=test_looger)
log_error('log_error', my_logger=test_looger)
log_debug('log_debug', my_logger=test_looger)
log_warn('log_warn', my_logger=test_looger)
