__author__ = 'baranbartu'

import logging
import threading
from memory_profiler import LineProfiler
from memgraph.profile import determine_memory_info

logger = logging.getLogger(__name__)


def observe(func=None, precision=1):
    if func is not None:
        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            val = prof(func)(*args, **kwargs)
            logger.info(
                'Please wait... Line graph will be ready in few seconds.')
            job = threading.Thread(target=determine_memory_info, args=(prof,),
                                   kwargs={'precision': precision})
            job.start()
            return val

        return wrapper
    else:
        def inner_wrapper(f):
            return observe(f, precision=precision)

        return inner_wrapper
