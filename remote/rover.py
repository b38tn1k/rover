import serial
import curses
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis
import datetime


def float2string(i):
    return '{:+06.2f}'.format(i)


def new_scatter(name, token):
    new_scatter = Scatter(
        x=[],
        y=[],
        name=name,
        showlegend=True,
        stream=dict(
            token=token,
            maxpoints=200
        )
    )
    return new_scatter


class rover(object):
    def __init__(self, address):
        self.address = address
        self.ir = {'FRONT': 0, 'REAR': 0}
        self.accel = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.gyro = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.compass = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.pose = {'X': 0, 'Y': 0, 'Z': 0}
        self.connected = False
        with open('stream_tokens.secret') as f:
            self.stream_tokens = f.readlines()

    def initialize_plotly(self):
        self.accelx_t = new_scatter('Accelerometer X', self.stream_tokens[1].rstrip())
        self.accely_t = new_scatter('Accelerometer Y', self.stream_tokens[2].rstrip())
        self.accelz_t = new_scatter('Accelerometer Z', self.stream_tokens[3].rstrip())
        layout = Layout(
            title='Rover1 Accelerometer',
            yaxis=YAxis(
                title='G forces (9.81ms^-2)',
                range=[-1.5, 1.5]
            )
        )
        data = Data([self.accelx_t, self.accely_t, self.accelz_t])
        fig = Figure(data=data, layout=layout)
        self.accelx_stream = py.Stream(self.stream_tokens[1].rstrip())
        self.accely_stream = py.Stream(self.stream_tokens[2].rstrip())
        self.accelz_stream = py.Stream(self.stream_tokens[3].rstrip())
        self.accelx_stream.open()
        self.accely_stream.open()
        self.accelz_stream.open()
        self.plotly_address = str(py.plot(fig, filename='Rover1 Accelerometer'))
        print(self.plotly_address)

    def update_plotly(self):
        now = datetime.datetime.now()
        self.accelx_stream.write({'x': now, 'y': self.accel['X']})
        self.accely_stream.write({'x': now, 'y': self.accel['Y']})
        self.accelz_stream.write({'x': now, 'y': self.accel['Z']})

    def connect(self):
        self.serial = serial.Serial('/dev/tty.usbserial-AJV9OOBQ', 38400)
        MOTD = ' '
        while True:
            MOTD = self.serial.readline()
            if 'Hello, World!' in MOTD:
                self.connected = True
                break
        self.accel['BIASX'] = float(self.serial.readline().rstrip())
        self.accel['BIASY'] = float(self.serial.readline().rstrip())
        self.accel['BIASZ'] = float(self.serial.readline().rstrip())
        self.gyro['BIASX'] = float(self.serial.readline().rstrip())
        self.gyro['BIASY'] = float(self.serial.readline().rstrip())
        self.gyro['BIASZ'] = float(self.serial.readline().rstrip())

    def read(self):
        self.serial.write("r")
        # Accelerometer
        self.accel['X'] = float(self.serial.readline().rstrip())
        self.accel['Y'] = float(self.serial.readline().rstrip())
        self.accel['Z'] = float(self.serial.readline().rstrip())
        # Gyro
        self.gyro['X'] = float(self.serial.readline().rstrip())
        self.gyro['Y'] = float(self.serial.readline().rstrip())
        self.gyro['Z'] = float(self.serial.readline().rstrip())
        # Compass
        self.compass['X'] = float(self.serial.readline().rstrip())
        self.compass['Y'] = float(self.serial.readline().rstrip())
        self.compass['Z'] = float(self.serial.readline().rstrip())
        # IR
        self.ir['FRONT'] = float(self.serial.readline().rstrip())
        self.ir['REAR'] = float(self.serial.readline().rstrip())

    def log2cli(self):
        print('Accelerometer')
        print(self.accel['X'])
        print(self.accel['Y'])
        print(self.accel['Z'])
        print('Gyro')
        print(self.gyro['X'])
        print(self.gyro['Y'])
        print(self.gyro['Z'])
        print('Compass')
        print(self.compass['X'])
        print(self.compass['Y'])
        print(self.compass['Z'])
        print('IR')
        print(self.ir['FRONT'])
        print(self.ir['REAR'])
        print(self.ir['REAR'] + self.ir['REAR'])

    def log2curses(self, screen, y_offset=3):
        dims = screen.getmaxyx()
        # ACCEL
        screen.addstr(y_offset + 0,        1,                       'Accelerometer', curses.A_BOLD)
        screen.addstr(y_offset + 1,        1,                       'X:', curses.A_DIM)
        screen.addstr(y_offset + 1,        dims[1]/3,               'Y:', curses.A_DIM)
        screen.addstr(y_offset + 1,        2*dims[1]/3,             'Z:', curses.A_DIM)
        screen.addstr(y_offset + 1,        4,                       float2string(self.accel['X']))
        screen.addstr(y_offset + 1,        (3 + dims[1]/3),         float2string(self.accel['Y']))
        screen.addstr(y_offset + 1,        (3 + 2*dims[1]/3),       float2string(self.accel['Z']))
        # GYRO
        screen.addstr(y_offset + 2,        1,                       'Gyroscope', curses.A_BOLD)
        screen.addstr(y_offset + 3,        1,                       'X:', curses.A_DIM)
        screen.addstr(y_offset + 3,        dims[1]/3,               'Y:', curses.A_DIM)
        screen.addstr(y_offset + 3,        2*dims[1]/3,             'Z:', curses.A_DIM)
        screen.addstr(y_offset + 3,        4,                       float2string(self.gyro['X']))
        screen.addstr(y_offset + 3,        (3 + dims[1]/3),         float2string(self.gyro['Y']))
        screen.addstr(y_offset + 3,        (3 + 2*dims[1]/3),       float2string(self.gyro['Z']))
        # COMPASS
        screen.addstr(y_offset + 4,        1,                       'Compass', curses.A_BOLD)
        screen.addstr(y_offset + 5,        1,                       'X:', curses.A_DIM)
        screen.addstr(y_offset + 5,        dims[1]/3,               'Y:', curses.A_DIM)
        screen.addstr(y_offset + 5,        2*dims[1]/3,             'Z:', curses.A_DIM)
        screen.addstr(y_offset + 5,        4,                       float2string(self.compass['X']))
        screen.addstr(y_offset + 5,        (3 + dims[1]/3),         float2string(self.compass['Y']))
        screen.addstr(y_offset + 5,        (3 + 2*dims[1]/3),       float2string(self.compass['Z']))
        # IR
        screen.addstr(y_offset + 6,        1,                        'IR', curses.A_BOLD)
        screen.addstr(y_offset + 7,        1,                        'F: ', curses.A_DIM)
        screen.addstr(y_offset + 7,        dims[1]/3,                'R: ', curses.A_DIM)
        screen.addstr(y_offset + 7,        4,                        float2string(self.ir['FRONT']))
        screen.addstr(y_offset + 7,        (3 + dims[1]/3),          float2string(self.ir['REAR']))
        screen.refresh()
