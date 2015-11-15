author__ = 'Baran Bartu Demici'
__version__ = '0.0.1'

import logging
from memgraph.functions import observe


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


@observe
def test_memory():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


if __name__ == '__main__':
    test_memory()
