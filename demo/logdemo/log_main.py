from yaoysTools.log.logutil import getLogger, log_info, log_error, log_warn, log_debug, MY_LOG_INFO, MY_LOG_DEBUG

test_looger = getLogger(log_name='test', save_log2_file=True, log_path='../../demo/log', is_only_file=False, log_level=MY_LOG_DEBUG)
log_info('log_info', my_logger=test_looger)
log_error('log_error', my_logger=test_looger)
log_debug('log_debug', my_logger=test_looger)
log_warn('log_warn', my_logger=test_looger)
