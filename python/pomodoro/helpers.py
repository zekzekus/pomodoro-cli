import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')


def get_filename(obj_id):
    return os.path.join(DATA_DIR, obj_id + '.obj')
