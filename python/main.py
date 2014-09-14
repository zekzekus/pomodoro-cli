# -*- coding: utf-8 -*-

import pickle
import os
from pomodoro import PomodoroTimer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')


def main():
    file_path = os.path.join(DATA_DIR, 'pomodoro.obj')
    try:
        f = open(file_path, 'r')
        p = pickle.load(f)
        f.close()
    except IOError:
        p = PomodoroTimer()
    finally:
        p.start()
        f = open(file_path, 'w')
        pickle.dump(p, f)
        f.close()


if __name__ == '__main__':
    main()
