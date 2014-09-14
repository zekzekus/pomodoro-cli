# -*- coding: utf-8 -*-
from progress.bar import Bar


class BaseOutputHandler(object):
    def ticking(self, status, counter, duration=None):
        raise NotImplemented

    def completed(self, count):
        raise NotImplemented


class StandardOutputHandler(BaseOutputHandler):
    def ticking(self, status, counter):
        print "{}: {}".format(status, counter)

    def completed(self, count):
        print "Completed pomodoros: {}".format(count)


class ProgressBarOutputHandler(BaseOutputHandler):
    def __init__(self, status, duration):
        self.bar = Bar(status, max=duration)
        self.finished = False

    def ticking(self, status, counter, duration):
        if self.finished:
            self.bar = Bar(status, max=duration)
            self.finished = False
        self.bar.next()

    def completed(self, count):
        print "\nCompleted pomodoros: {}".format(count)
        self.bar.finish()
        self.finished = True
