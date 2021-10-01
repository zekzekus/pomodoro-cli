# -*- coding: utf-8 -*-

import sys

from pomodoro import PomodoroTimer
from pomodoro.exceptions import PomodoroTimerNotFound


def main(args):
    id = args[1] if len(args) > 1 else None

    try:
        p = PomodoroTimer.loads(id=id)
    except PomodoroTimerNotFound:
        p = PomodoroTimer()
        print(f"timer not found with id: {id}. new timer created with id: {p.id}")

    p.start()
    p.dumps()


if __name__ == '__main__':
    main(sys.argv)
