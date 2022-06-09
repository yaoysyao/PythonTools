import logging

from yaoysTools.log.logutil import getLogger
from yaoysTools.log.logutil import log_info
from yaoysTools.log.logutil import log_warn
from yaoysTools.log.logutil import log_error

import yaoysTools.log.logutil as log

log_test = getLogger(log_name='log_test', log_path='./log', save_log2_file=True, log_level=log.MY_LOG_DEBUG)
log_info('test', my_logger=log_test)
log_error('error', my_logger=log_test)
