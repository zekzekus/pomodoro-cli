# -*- coding: utf-8 -*-


class BaseOutputHandler(object):
    def ticking(self, status, counter):
        raise NotImplemented

    def work_completed(self, count):
        raise NotImplemented


class StandardOutputHandler(BaseOutputHandler):
    def ticking(self, status, counter):
        print "{}: {}".format(status, counter)

    def work_completed(self, count):
        print "Completed pomodoros: {}".format(count)
