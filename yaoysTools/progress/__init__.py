# Copyright (c) 2012 Georgios Verigakis <verigak@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# The github url: https://github.com/verigak/progress.git

from __future__ import division, print_function

from collections import deque
from datetime import timedelta
from math import ceil
from sys import stderr
from yaoysTools.log.logutil import MY_LOG_DEBUG, log_info, log_error, log_warn, \
    log_debug, MY_LOG_INFO, MY_LOG_ERROR, MY_LOG_WARN, get_log_level

try:
    from time import monotonic
except ImportError:
    from time import time as monotonic

__version__ = '1.6'

HIDE_CURSOR = '\x1b[?25l'
SHOW_CURSOR = '\x1b[?25h'

'''
The show time type is : avg:	simple moving average time per item (in seconds)
                        elapsed:	elapsed time in seconds
                        elapsed_td:	elapsed as a timedelta (useful for printing as a string)
                        eta:	avg * remaining
                        eta_td:	eta as a timedelta (useful for printing as a string)
if you want to define the show time type,you must set the need_show_time is True

if you use spinner,you don't use eta and eta_td
'''


class Infinite(object):
    file = stderr
    sma_window = 10  # Simple Moving Average window
    check_tty = True
    hide_cursor = True

    def __init__(self, message='', **kwargs):
        self.index = 0
        self.start_ts = monotonic()
        self.avg = 0
        self._avg_update_ts = self.start_ts
        self._ts = self.start_ts
        self._xput = deque(maxlen=self.sma_window)

        self._max_width = 0
        self._hidden_cursor = False
        self.message = message

        self.is_save_log = kwargs.get('is_save_log', False)
        self.logger = kwargs.get('logger', None)
        self.check_tty = kwargs.get('check_tty', False)
        self.need_show_time = kwargs.get('need_show_time', True)
        self.show_time_type = kwargs.get('show_time_type', 'elapsed_td')
        if self.logger is not None:
            self.log_level = get_log_level(my_logger=self.logger)
        else:
            self.log_level = MY_LOG_DEBUG

        if self.file and self.is_tty():
            if self.hide_cursor:
                print(HIDE_CURSOR, end='', file=self.file)
                self._hidden_cursor = True
        self.writeln('')

    def __del__(self):
        if self._hidden_cursor:
            print(SHOW_CURSOR, end='', file=self.file)

    def __getitem__(self, key):
        if key.startswith('_'):
            return None
        return getattr(self, key, None)

    @property
    def elapsed(self):
        return int(monotonic() - self.start_ts)

    @property
    def elapsed_td(self):
        return timedelta(seconds=self.elapsed)

    def update_avg(self, n, dt):
        if n > 0:
            xput_len = len(self._xput)
            self._xput.append(dt / n)
            now = monotonic()
            # update when we're still filling _xput, then after every second
            if (xput_len < self.sma_window or
                    now - self._avg_update_ts > 1):
                self.avg = sum(self._xput) / len(self._xput)
                self._avg_update_ts = now

    def update(self):
        pass

    def start(self):
        pass

    def writeln(self, line):
        if self.file and self.is_tty():
            width = len(line)
            if width < self._max_width:
                # Add padding to cover previous contents
                line += ' ' * (self._max_width - width)
            else:
                self._max_width = width
            print('\r' + line, end='', file=self.file)
            self.file.flush()

            if self.is_save_log is True:
                if self.log_level == MY_LOG_DEBUG:
                    log_debug(line, my_logger=self.logger)
                if self.log_level == MY_LOG_INFO:
                    log_info(line, my_logger=self.logger)
                if self.log_level == MY_LOG_ERROR:
                    log_error(line, my_logger=self.logger)
                if self.log_level == MY_LOG_WARN:
                    log_warn(line, my_logger=self.logger)

    def finish(self):
        if self.file and self.is_tty():
            print(file=self.file)
            if self._hidden_cursor:
                print(SHOW_CURSOR, end='', file=self.file)
                self._hidden_cursor = False

    def is_tty(self):
        try:
            return self.file.isatty() if self.check_tty else True
        except AttributeError:
            msg = "%s has no attribute 'isatty'. Try setting check_tty=False." % self
            raise AttributeError(msg)

    def next(self, n=1):
        now = monotonic()
        dt = now - self._ts
        self.update_avg(n, dt)
        self._ts = now
        self.index = self.index + n
        self.update()

    def iter(self, it):
        self.iter_value = None
        with self:
            for x in it:
                self.iter_value = x
                yield x
                self.next()
        del self.iter_value

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()


class Progress(Infinite):
    def __init__(self, *args, **kwargs):
        super(Progress, self).__init__(*args, **kwargs)
        self.max = kwargs.get('max', 100)

    @property
    def eta(self):
        return int(ceil(self.avg * self.remaining))

    @property
    def eta_td(self):
        return timedelta(seconds=self.eta)

    @property
    def percent(self):
        return self.progress * 100

    @property
    def progress(self):
        if self.max == 0:
            return 0
        return min(1, self.index / self.max)

    @property
    def remaining(self):
        return max(self.max - self.index, 0)

    def start(self):
        self.update()

    def goto(self, index):
        incr = index - self.index
        self.next(incr)

    def iter(self, it):
        try:
            self.max = len(it)
        except TypeError:
            pass

        self.iter_value = None
        with self:
            for x in it:
                self.iter_value = x
                yield x
                self.next()
        del self.iter_value
