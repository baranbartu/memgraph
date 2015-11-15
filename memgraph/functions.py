__author__ = 'baranbartu'

import os
import inspect
import linecache
import logging
import csv
import threading
from memory_profiler import LineProfiler
from memgraph.utils import generate_file_name
from memgraph.plot import make_plot

logger = logging.getLogger(__name__)


def observe(f):
    def wrapper(*args, **kwargs):
        prof = LineProfiler()
        val = prof(f)(*args, **kwargs)
        logger.info('Please wait... Line graph will be ready in few seconds.')
        job = threading.Thread(target=make_line_graph, args=(prof,))
        job.start()
        return val

    return wrapper


def make_line_graph(prof, precision=1):
    logs = {}
    for code in prof.code_map:
        lines = prof.code_map[code]
        if not lines:
            # .. measurements are empty ..
            continue
        filename = code.co_filename
        if filename.endswith((".pyc", ".pyo")):
            filename = filename[:-1]
        logger.debug('Filename: ' + filename + '\n\n')
        if not os.path.exists(filename):
            logger.error('ERROR: Could not find file ' + filename + '\n')
            if any([filename.startswith(k) for k in
                    ("ipython-input", "<ipython-input")]):
                logger.info(
                    "NOTE: memgraph can only be used on functions defined in "
                    "physical files, and not in the IPython environment.")
            continue
        all_lines = linecache.getlines(filename)
        sub_lines = inspect.getblock(all_lines[code.co_firstlineno - 1:])
        linenos = range(code.co_firstlineno,
                        code.co_firstlineno + len(sub_lines))

        mem_old = lines[min(lines.keys())]
        float_format = '{0}.{1}f'.format(precision + 4, precision)
        template_mem = '{0:' + float_format + '}'
        for line in linenos:
            if line in lines:
                mem = lines[line]
                inc = mem - mem_old
                mem_old = mem
                mem = template_mem.format(mem)
                inc = template_mem.format(inc)
                # todo will be used in the future to make more sensitive
                values = (line, mem, inc, all_lines[line - 1])
                logs[line] = inc
        # todo will be used in the future
        csv_file = make_csv(logs)
        make_plot(logs, csv_file.replace('.csv', ''))
        # todo remove csv file


def make_csv(logs):
    csv_file = '%s.csv' % generate_file_name()
    with open(csv_file, 'w') as csvfile:
        fieldnames = ['Line', 'Increase']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in sorted(logs.keys()):
            writer.writerow({'Line': str(line), 'Increase': str(logs[line])})
    return csv_file
