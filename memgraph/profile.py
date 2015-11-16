__author__ = 'baranbartu'

import os
import logging
import inspect
import linecache
from memgraph.plot import make_plot
from memgraph.utils import make_csv, remove_file

logger = logging.getLogger(__name__)


def determine_memory_info(prof, precision=1):
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
                logs[line] = mem
        # todo will be used in the future
        csv_file = make_csv(logs, ['Line', 'Memory'])
        make_plot(logs, csv_file.replace('.csv', ''))
        remove_file(csv_file)
