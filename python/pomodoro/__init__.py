# -*- coding: utf-8 -*-
import time

from hashids import Hashids

from .handlers import ProgressBarOutputHandler
from .backends import PicklePersistenceBackend

STATUS_WORK = 'work'
STATUS_SHORT_REST = 'short'
STATUS_LONG_REST = 'long'

DEFAULT_BACKEND = PicklePersistenceBackend
ID_SALT = 'T*{VghkFo}2lcknb~Np$s8+$^|n~>59~#,+D9Z3Eaq/n+'
ID_ALPHABET = '1234567890ABCDEF'


class PomodoroTimer(object):
    def __init__(self, work_duration=4, short_rest=2, long_rest=3,
                 output_handler_cls=ProgressBarOutputHandler,
                 backend_cls=DEFAULT_BACKEND,
                 id=None):
        self.id = self.__generate_id() if not id else id
        self.durations = {
            STATUS_WORK: work_duration,
            STATUS_SHORT_REST: short_rest,
            STATUS_LONG_REST: long_rest
        }
        self.output_handler = output_handler_cls(self.id, STATUS_WORK,
                                                 duration=work_duration)
        self.backend = backend_cls(self.id)
        self.session_count = 0
        self.status = STATUS_WORK

    def __generate_id(self):
        hashids = Hashids(salt=ID_SALT, alphabet=ID_ALPHABET, min_length=6)
        return hashids.encrypt(int(time.time()))

    def start(self):
        counter = self._counter

        while counter > 0:
            self.ticking(counter)
            counter -= 1
            time.sleep(1)

        self.timer_completed()
        self._next_status()

    def timer_completed(self):
        if self.is_working:
            self.session_count += 1
        self.output_handler.completed(self.session_count)

    def ticking(self, counter):
        self.output_handler.ticking(self.status, counter, self._counter)

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
        if self.is_working:
            if self.session_count % 4 == 0:
                self.status = STATUS_LONG_REST
            else:
                self.status = STATUS_SHORT_REST
        else:
            self.status = STATUS_WORK

        return self.status

    @property
    def _counter(self):
        return self.durations[self.status]

    def dumps(self):
        self.backend.dumps(self)

    @classmethod
    def loads(klass, id, backend_cls=DEFAULT_BACKEND):
        backend = backend_cls(id)
        return backend.loads()
