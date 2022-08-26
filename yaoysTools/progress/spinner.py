# -*- coding: utf-8 -*-

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
from __future__ import unicode_literals
from . import Infinite


class Spinner(Infinite):
    phases = ('-', '\\', '|', '/')
    hide_cursor = True

    time_suffix = ' %(elapsed_td)ds '
    bar_time = ''

    def update(self):
        i = self.index % len(self.phases)
        message = self.message % self
        self.get_show_time()
        line = ''.join([message, self.phases[i], self.bar_time])
        self.writeln(line)

    def get_show_time(self):
        if self.need_show_time is False:
            self.bar_time = ''
        else:
            if self.show_time_type == 'elapsed':
                self.time_suffix = ' %(elapsed)ds '
                self.bar_time = self.time_suffix % self
            elif self.show_time_type == 'eta':
                self.time_suffix = ' %(eta)ds '
                self.bar_time = self.time_suffix % self
            elif self.show_time_type == 'elapsed_td':
                self.bar_time = ' ' + str(self.elapsed_td) + ' '
            elif self.show_time_type == 'eta_td':
                self.bar_time = ' '


class PieSpinner(Spinner):
    phases = ['◷', '◶', '◵', '◴']


class MoonSpinner(Spinner):
    phases = ['◑', '◒', '◐', '◓']


class LineSpinner(Spinner):
    phases = ['⎺', '⎻', '⎼', '⎽', '⎼', '⎻']


class PixelSpinner(Spinner):
    phases = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
