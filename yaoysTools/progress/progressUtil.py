from time import sleep

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


class definitionProgressBar(object):
    def __init__(self, progress_type=PROGRESS_TYPE_BAR, count=0, message='Progress', check_tty=False, is_save_log=False, logger=None, log_path=None):
        self.progress_type = progress_type
        self.count = count
        self.message = message
        self.check_tty = check_tty
        self.is_save_log = is_save_log
        self.logger = logger
        self.log_path = log_path

        if self.is_save_log is True and self.logger is None:
            if self.log_path is None:
                raise Exception('The log_path is not None,if you want to save the progress to log')
            self.logger = getLogger(self.message, log_level=MY_LOG_INFO, log_path=self.log_path, is_only_file=True)

    def get_progress(self):
        if self.progress_type == PROGRESS_TYPE_BAR:
            return Bar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_CHARGING_BAR:
            return ChargingBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_FILLINGSQUARESBAR:
            return FillingSquaresBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_FILLINGCIRCLESBAR:
            return FillingCirclesBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_INCREMENTALBAR:
            return IncrementalBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_PIXELBAR:
            return PixelBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)
        if self.progress_type == PROGRESS_TYPE_SHADYBAR:
            return ShadyBar(self.message, max=self.count, check_tty=self.check_tty, is_save_log=self.is_save_log, logger=self.logger)

        if self.progress_type == PROGRESS_TYPE_SPINNER:
            return Spinner(self.message, check_tty=self.check_tty, is_save_log=False)
        if self.progress_type == PROGRESS_TYPE_PIESPINNER:
            return PieSpinner(self.message, check_tty=self.check_tty, is_save_log=False)
        if self.progress_type == PROGRESS_TYPE_MOONSPINNER:
            return MoonSpinner(self.message, check_tty=self.check_tty, is_save_log=False)
        if self.progress_type == PROGRESS_TYPE_LINESPINNER:
            return LineSpinner(self.message, check_tty=self.check_tty, is_save_log=False)
        if self.progress_type == PROGRESS_TYPE_PIXELSPINNER:
            return PixelSpinner(self.message, check_tty=self.check_tty, is_save_log=False)


if __name__ == '__main__':
    bar = definitionProgressBar(progress_type=PROGRESS_TYPE_PIXELBAR,
                                count=100, is_save_log=True, log_path='../../demo/log').get_progress()
    for i in range(100):
        # Do some work
        sleep(0.01)
        bar.next()
    bar.finish()
