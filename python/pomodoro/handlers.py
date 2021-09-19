# -*- coding: utf-8 -*-
from progress.bar import Bar


class BaseOutputHandler(object):
    def __init__(self, id, status, duration):
        self.id = id

    def ticking(self, status, counter, duration=None):
        raise NotImplementedError

    def completed(self, count):
        raise NotImplementedError


class StandardOutputHandler(BaseOutputHandler):
    def ticking(self, status, counter, duration):
        print "{}({}): {}".format(status, self.id, counter)

    def completed(self, count):
        print "Completed pomodoros ({}): {}".format(self.id, count)


class ProgressBarOutputHandler(BaseOutputHandler):
    def __init__(self, id, status, duration):
        super(ProgressBarOutputHandler, self).__init__(id)
        self.bar = Bar(status, max=duration)
        self.finished = False

    def ticking(self, status, counter, duration):
        if self.finished:
            self.bar = Bar(status, max=duration)
            self.finished = False
        self.bar.next()

    def completed(self, count):
        print "\nCompleted pomodoros ({}): {}".format(self.id, count)
        self.bar.finish()
        self.finished = True
