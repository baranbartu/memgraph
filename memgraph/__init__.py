author__ = 'Baran Bartu Demici'
__version__ = '0.0.1'

import time
from memgraph.daemon import Daemon
from guppy import hpy

d = Daemon()
logs = {}


def observe_memory(f):
    def wrapper(*args, **kwargs):
        wait = kwargs.get('wait', 0.0000000001)
        d.start(memory_info_daemon, (logs, wait))
        f(*args, **kwargs)
        d.stop()
        # todo make a plot from csv logs

    return wrapper


def memory_info_daemon(logs, wait, stop):
    while not stop.is_set():
        info = hpy().heap()
        # todo add info to logs
        # todo convert to csv
        time.sleep(wait)

