from yaoysTools.log.logutil import getLogger
from yaoysTools.log.logutil import log_info
from yaoysTools.log.logutil import MY_LOG_INFO

logger = getLogger(log_name='testMain', save_log2_file=True, log_level=MY_LOG_INFO, log_path='./demo/log')
log_info('test', my_logger=logger)
