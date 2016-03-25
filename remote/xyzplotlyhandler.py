# James Carthew March 2016
# simple streaming x/y/z scatter plot contructor
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis
import datetime
from time import sleep


def new_scatter(name, token):
    new_scatter = Scatter(
        x=[],
        y=[],
        name=name,
        showlegend=True,
        stream=dict(
            token=token,
            maxpoints=500
        )
    )
    return new_scatter


class XYZPlotlyHandler(object):
    def __init__(self, project_title, name, first_token, units, symm_range):
        with open('stream_tokens.secret') as f:
            stream_tokens = f.readlines()
        x_token = stream_tokens[first_token].rstrip()
        y_token = stream_tokens[first_token + 1].rstrip()
        z_token = stream_tokens[first_token + 2].rstrip()
        x_scatter = new_scatter('{} X'.format(name), x_token)
        y_scatter = new_scatter('{} Y'.format(name), y_token)
        z_scatter = new_scatter('{} Z'.format(name), z_token)
        layout = Layout(
            # showlegend=True,
            title='{}: {}'.format(project_title, name),
            yaxis=YAxis(
                title=units,
                range=[0-symm_range, symm_range]
            )
        )
        data = Data([x_scatter, y_scatter, z_scatter])
        fig = Figure(data=data, layout=layout)
        self.x_stream = py.Stream(x_token)
        self.y_stream = py.Stream(y_token)
        self.z_stream = py.Stream(z_token)
        self.x_stream.open()
        self.y_stream.open()
        self.z_stream.open()
        self.plotly_address = py.plot(fig, filename='{}: {}'.format(project_title, name))

    def update(self, data2plot):
        now = datetime.datetime.now()
        self.x_stream.write({'x': now, 'y': data2plot['X']})
        self.y_stream.write({'x': now, 'y': data2plot['Y']})
        self.z_stream.write({'x': now, 'y': data2plot['Z']})
        sleep(0.1)

    def close_streams(self):
        self.x_stream.close()
        self.y_stream.close()
        self.z_stream.close()
