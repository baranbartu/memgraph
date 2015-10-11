author__ = 'Baran Bartu Demici'
__version__ = '0.0.1'

import time
import logging
from memgraph.daemon import Daemon, Logic
from guppy import hpy


class ExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(ExceptionFormatter, self).formatException(exc_info)
        return repr(result)

    def format(self, record):
        s = super(ExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '')
        return s


logger = logging.getLogger('memgraph')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
fmt = '%(levelname)s %(asctime)s memgraph pid-%(process)d %(message)s'
formatter = ExceptionFormatter(fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)


class DefaultMemoryLogic(Logic):
    def execute(self):
        memory = hpy().heap()
        self.logs[time.time()] = memory
        # todo update logs correctly

    def logs_to_csv(self):
        logger.info(self.logs)
        # todo convert logs to csv

    def make_plot(self):
        logger.info('make a plot.')
        # todo make a plot


def observe(f, wait=0.0000000001, generate_csv=True, make_plot=False):
    def wrapper(*args, **kwargs):
        d = Daemon(DefaultMemoryLogic())
        d.start((wait,))
        f(*args, **kwargs)
        d.stop(generate_csv, make_plot)

    return wrapper
