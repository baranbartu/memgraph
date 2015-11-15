__author__ = 'baranbartu'

import logging
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

logger = logging.getLogger(__name__)


def make_plot(logs, file_name):
    plotly.tools.set_credentials_file(username='memgraph',
                                      api_key='wb1kstdv2f')
    x = [line for line in sorted(logs.keys())]
    y = [logs[line] for line in sorted(logs.keys())]
    trace = go.Scatter(
        x=x,
        y=y
    )
    data = [trace]

    plot_url = py.plot(data, filename=file_name, share='public')
    logger.info('Please visit this url: %s', plot_url)
