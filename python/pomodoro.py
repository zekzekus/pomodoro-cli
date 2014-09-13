# -*- coding: utf-8 -*-
import time

STATUS_WORK = 'work'
STATUS_SHORT_REST = 'short'
STATUS_LONG_REST = 'long'


class PomodoroTimer(object):
    def __init__(self, work_duration=4, short_rest=2, long_rest=3):
        self.work_duration = work_duration
        self.short_rest = short_rest
        self.long_rest = long_rest
        self.session_count = 0
        self.status = STATUS_WORK

    def start(self):
        counter = self._counter()

        while counter > 0:
            print "%s: %d" % (self.status, counter)
            counter -= 1
            time.sleep(1)

        if self.is_working:
            self.session_count += 1
        self._next_status()

    @property
    def is_working(self):
        return self.status == STATUS_WORK

    @property
    def is_short_rest(self):
        return self.status == STATUS_SHORT_REST

    @property
    def is_long_rest(self):
        return self.status == STATUS_LONG_REST

    def _next_status(self):
        if self.status == STATUS_WORK:
            if self.session_count % 4 == 0:
                self.status = STATUS_LONG_REST
            else:
                self.status = STATUS_SHORT_REST
        else:
            self.status = STATUS_WORK

        return self.status

    def _counter(self):
        if self.status == STATUS_WORK:
            counter = self.work_duration
        elif self.status == STATUS_SHORT_REST:
            counter = self.short_rest
        elif self.status == STATUS_LONG_REST:
            counter = self.long_rest

        return counter
