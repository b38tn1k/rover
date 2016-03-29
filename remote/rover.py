import serial
import curses
from time import sleep
from xyzplotlyhandler import XYZPlotlyHandler


def float2string(i):
    return '{:+06.2f}'.format(i)


class Rover(object):
    def __init__(self, address):
        self.address = address
        self.ir = {'FRONT': 0, 'REAR': 0}
        self.accel = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.gyro = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.compass = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.pose = {'X': 0, 'Y': 0, 'Z': 0}
        self.connected = False
        self.accel_plot = None
        self.gyro_plot = None
        self.compass_plot = None
        self.message_length = 0  # Set by Arduino upon connect
        self.message_number = 0

    def plot_accel(self):
        if self.accel_plot is None:
            self.accel_plot = XYZPlotlyHandler("Rover1", "Accelerometer Data", 0, "G-FORCES", 1.5)
        else:
            self.accel_plot.update(self.accel)

    def plot_compass(self):
        if self.compass_plot is None:
            self.compass_plot = XYZPlotlyHandler("Rover1", "Compass Data", 3, "DEGREES", 180)
        else:
            self.compass_plot.update(self.compass)

    def plot_gyro(self):
        if self.gyro_plot is None:
            self.gyro_plot = XYZPlotlyHandler("Rover1", "Gyro Data", 7, "DEGREES/SEC", 180)
        else:
            self.gyro_plot.update(self.gyro)

    def connect(self):
        self.serial = serial.Serial('/dev/tty.usbserial-AJV9OOBQ', 38400)
        MOTD = ' '
        while True:
            MOTD = self.serial.readline()
            if 'Hello, World!' in MOTD:
                self.connected = True
                break
        # self.message_length = int(self.serial.readline().rstrip())
        # self.accel['BIASX'] = float(self.serial.readline().rstrip())
        # self.accel['BIASY'] = float(self.serial.readline().rstrip())
        # self.accel['BIASZ'] = float(self.serial.readline().rstrip())
        # self.gyro['BIASX'] = float(self.serial.readline().rstrip())
        # self.gyro['BIASY'] = float(self.serial.readline().rstrip())
        # self.gyro['BIASZ'] = float(self.serial.readline().rstrip())

    def write(self, msg):
        # need to look into bytearray

        # +--------+----------------+---------+------>
        # | Header | Message Length | Data ID | Data
        # +--------+----------------+---------+------>
        new_message = '~er'
        self.serial.write(new_message)

    def read(self):
        self.write('r')
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
        clear = [' '] * (dims[1] - 1)
        delimiter = ['-'] * len(clear)
        clear = ''.join(clear)
        delimiter = ''.join(delimiter)
        for i in range(0, 8):
            screen.addstr(y_offset + i, 1, clear)
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
        # END OF OUPUT
        screen.addstr(y_offset + 8, 1, delimiter)
        screen.refresh()
        return (y_offset + 9)
