import pickle

from .helpers import get_filename
from .exceptions import PomodoroTimerNotFound


class BasePersistenceBackend(object):
    def __init__(self, id):
        self.id = id
        self.filename = get_filename(id) if self.id is not None else None

    def loads(self):
        raise NotImplementedError

    def dumps(self, pomodoro_obj):
        raise NotImplementedError


class PicklePersistenceBackend(BasePersistenceBackend):
    def dumps(self, pomodoro_obj):
        f = open(self.filename, 'w')
        pickle.dump(pomodoro_obj, f)
        f.close()

    def loads(self):
        if not self.id:
            raise PomodoroTimerNotFound('supply an id to load')
        try:
            f = open(self.filename, 'r')
            p = pickle.load(f)
            f.close()
            return p
        except IOError:
            raise PomodoroTimerNotFound(
                'Pomodoro timer not found: {}'.format(id))
