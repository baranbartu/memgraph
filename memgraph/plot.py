__author__ = 'baranbartu'

import logging
import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go

logger = logging.getLogger(__name__)


def make_plot(logs, file_name):
    tls.set_credentials_file(username='memgraph',
                                      api_key='wb1kstdv2f')
    x = [line['x'] for line in sorted(logs, key=lambda l: l['x'])]
    y = [line['y'] for line in sorted(logs, key=lambda l: l['x'])]
    trace = go.Scatter(
        x=x,
        y=y
    )
    data = [trace]

    plot_url = py.plot(data, filename=file_name, share='public')
    logger.info('Please visit this url: %s', plot_url)
