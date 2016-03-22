import serial
import matplotlib
import curses


class rover(object):
    def __init__(self, address):
        self.address = address
        self.ir = {'FRONT': 0, 'REAR': 0}
        self.accel = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.gyro = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.compass = {'X': 0, 'Y': 0, 'Z': 0, 'BIASX': 0, 'BIASY': 0, 'BIASZ': 0}
        self.pose = {'X': 0, 'Y': 0, 'Z': 0}
        self.connected = False

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
        screen.addstr(y_offset + 1,        4,                       "{0:.2f}".format(self.accel['X']))
        screen.addstr(y_offset + 1,        (3 + dims[1]/3),         "{0:.2f}".format(self.accel['Y']))
        screen.addstr(y_offset + 1,        (3 + 2*dims[1]/3),       "{0:.2f}".format(self.accel['Z']))
        # GYRO
        screen.addstr(y_offset + 2,        1,                       'Gyroscope', curses.A_BOLD)
        screen.addstr(y_offset + 3,        1,                       'X:', curses.A_DIM)
        screen.addstr(y_offset + 3,        dims[1]/3,               'Y:', curses.A_DIM)
        screen.addstr(y_offset + 3,        2*dims[1]/3,             'Z:', curses.A_DIM)
        screen.addstr(y_offset + 3,        4,                       "{0:.2f}".format(self.gyro['X']))
        screen.addstr(y_offset + 3,        (3 + dims[1]/3),         "{0:.2f}".format(self.gyro['Y']))
        screen.addstr(y_offset + 3,        (3 + 2*dims[1]/3),       "{0:.2f}".format(self.gyro['Z']))
        # COMPASS
        screen.addstr(y_offset + 4,        1,                       'Compass', curses.A_BOLD)
        screen.addstr(y_offset + 5,        1,                       'X:', curses.A_DIM)
        screen.addstr(y_offset + 5,        dims[1]/3,               'Y:', curses.A_DIM)
        screen.addstr(y_offset + 5,        2*dims[1]/3,             'Z:', curses.A_DIM)
        screen.addstr(y_offset + 5,        4,                       "{0:.2f}".format(self.compass['X']))
        screen.addstr(y_offset + 5,        (3 + dims[1]/3),         "{0:.2f}".format(self.compass['Y']))
        screen.addstr(y_offset + 5,        (3 + 2*dims[1]/3),       "{0:.2f}".format(self.compass['Z']))
        # IR
        screen.addstr(y_offset + 6,        1,                        'IR', curses.A_BOLD)
        screen.addstr(y_offset + 7,        1,                        'F: ', curses.A_DIM)
        screen.addstr(y_offset + 7,        dims[1]/3,                'R: ', curses.A_DIM)
        screen.addstr(y_offset + 7,        3,                        "{0:.2f}".format(self.ir['FRONT']))
        screen.addstr(y_offset + 7,        (3 + dims[1]/3),          "{0:.2f}".format(self.ir['REAR']))
        screen.refresh()
