# -*- coding: UTF-8 -*-

from yaoysTools.log.logutil import MY_LOG_INFO, getLogger
from yaoysTools.progress.bar import Bar, ChargingBar, FillingCirclesBar, FillingSquaresBar, IncrementalBar, PixelBar, ShadyBar
from yaoysTools.progress.spinner import LineSpinner, MoonSpinner, PieSpinner, PixelSpinner, Spinner

PROGRESS_TYPE_BAR = 'Bar'
PROGRESS_TYPE_CHARGING_BAR = 'ChargingBar'
PROGRESS_TYPE_FILLINGSQUARESBAR = 'FillingSquaresBar'
PROGRESS_TYPE_FILLINGCIRCLESBAR = 'FillingCirclesBar'
PROGRESS_TYPE_INCREMENTALBAR = 'IncrementalBar'
PROGRESS_TYPE_PIXELBAR = 'PixelBar'
PROGRESS_TYPE_SHADYBAR = 'ShadyBar'
PROGRESS_TYPE_SPINNER = 'Spinner'
PROGRESS_TYPE_PIESPINNER = 'PieSpinner'
PROGRESS_TYPE_MOONSPINNER = 'MoonSpinner'
PROGRESS_TYPE_LINESPINNER = 'LineSpinner'
PROGRESS_TYPE_PIXELSPINNER = 'PixelSpinner'

# The show time type
# elapsed	elapsed time in seconds such as: 10s
# elapsed_td	elapsed as a timedelta (useful for printing as a string) such as: 0:00:15
# eta	avg * remaining such as 10s,9s,8s.....
# eta_td	eta as a timedelta (useful for printing as a string) such as 0:00:15,0:00:14,0:00:13...

PROGRESS_ELAPSED = 'elapsed'
PROGRESS_ELAPSED_TD = 'elapsed_td'
PROGRESS_ETA = 'eta'
PROGRESS_ETA_TD = 'eta_td'


class definitionProgress(object):
    def __init__(self, **kwargs):
        self.progress_type = kwargs.get('progress_type', PROGRESS_TYPE_BAR)
        self.count = kwargs.get('count', 0)
        self.message = kwargs.get('message', 'Progress')
        self.check_tty = kwargs.get('check_tty', False)
        self.is_save_log = kwargs.get('is_save_log', False)
        self.logger = kwargs.get('logger', None)
        self.log_path = kwargs.get('log_path', None)
        self.__progress_color = kwargs.get('progress_color', None)
        self.__need_show_time = kwargs.get('need_show_time', True)
        self.__show_time_type = kwargs.get('show_time_type', PROGRESS_ELAPSED_TD)

        if self.progress_type in (PROGRESS_TYPE_SPINNER, PROGRESS_TYPE_MOONSPINNER, PROGRESS_TYPE_PIESPINNER, PROGRESS_TYPE_LINESPINNER, PROGRESS_TYPE_PIESPINNER) \
                and self.__show_time_type in (PROGRESS_ETA, PROGRESS_ETA_TD):
            raise Exception("if you use spinner,you don't use eta and eta_td")
        if self.is_save_log is True and self.logger is None:
            if self.log_path is None:
                raise Exception('The log_path is not None,if you want to save the progress to log')
            self.logger = getLogger(self.message, log_level=MY_LOG_INFO, log_path=self.log_path, is_only_file=True)

    def get_progress(self):
        if self.progress_type == PROGRESS_TYPE_BAR:
            return Bar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_CHARGING_BAR:
            return ChargingBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_FILLINGSQUARESBAR:
            return FillingSquaresBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_FILLINGCIRCLESBAR:
            return FillingCirclesBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_INCREMENTALBAR:
            return IncrementalBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_PIXELBAR:
            return PixelBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_SHADYBAR:
            return ShadyBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger, color=self.__progress_color, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)

        if self.progress_type == PROGRESS_TYPE_SPINNER:
            return Spinner(self.message, check_tty=self.check_tty, is_save_log=False, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_PIESPINNER:
            return PieSpinner(self.message, check_tty=self.check_tty, is_save_log=False, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_MOONSPINNER:
            return MoonSpinner(self.message, check_tty=self.check_tty, is_save_log=False, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_LINESPINNER:
            return LineSpinner(self.message, check_tty=self.check_tty, is_save_log=False, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
        if self.progress_type == PROGRESS_TYPE_PIXELSPINNER:
            return PixelSpinner(self.message, check_tty=self.check_tty, is_save_log=False, need_show_time=self.__need_show_time, show_time_type=self.__show_time_type)
