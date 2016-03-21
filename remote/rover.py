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
        self.accel['BIASX'] = self.serial.readline().rstrip()
        self.accel['BIASY'] = self.serial.readline().rstrip()
        self.accel['BIASZ'] = self.serial.readline().rstrip()
        self.gyro['BIASX'] = self.serial.readline().rstrip()
        self.gyro['BIASY'] = self.serial.readline().rstrip()
        self.gyro['BIASZ'] = self.serial.readline().rstrip()

    def read(self):
        self.serial.write("r")
        # Accelerometer
        self.accel['X'] = self.serial.readline().rstrip()
        self.accel['Y'] = self.serial.readline().rstrip()
        self.accel['Z'] = self.serial.readline().rstrip()
        # Gyro
        self.gyro['X'] = self.serial.readline().rstrip()
        self.gyro['Y'] = self.serial.readline().rstrip()
        self.gyro['Z'] = self.serial.readline().rstrip()
        # Compass
        self.compass['X'] = self.serial.readline().rstrip()
        self.compass['Y'] = self.serial.readline().rstrip()
        self.compass['Z'] = self.serial.readline().rstrip()
        # IR
        self.ir['FRONT'] = self.serial.readline().rstrip()
        self.ir['REAR'] = self.serial.readline().rstrip()

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

    def log2curses(self, screen, xmax):
        # ACCEL
        screen.addstr(3,        1,                  'Accelerometer')
        screen.addstr(4,        1,                  'X:')
        screen.addstr(4,        xmax/3,             'Y:')
        screen.addstr(4,        2*xmax/3,           'Z:')
        screen.addstr(4,        4,                  self.accel['X'])
        screen.addstr(4,        (3 + xmax/3),       self.accel['Y'])
        screen.addstr(4,        (3 + 2*xmax/3),     self.accel['Z'])
        # GYRO
        screen.addstr(5,        1,                  'Gyroscope')
        screen.addstr(6,        1,                  'X:')
        screen.addstr(6,        xmax/3,             'Y:')
        screen.addstr(6,        2*xmax/3,           'Z:')
        screen.addstr(6,        4,                  self.gyro['X'])
        screen.addstr(6,        (3 + xmax/3),       self.gyro['Y'])
        screen.addstr(6,        (3 + 2*xmax/3),     self.gyro['Z'])
        # COMPASS
        screen.addstr(7,        1,                  'Compass')
        screen.addstr(8,        1,                  'X:')
        screen.addstr(8,        xmax/3,             'Y:')
        screen.addstr(8,        2*xmax/3,           'Z:')
        screen.addstr(8,        4,                  self.compass['X'])
        screen.addstr(8,        (3 + xmax/3),       self.compass['Y'])
        screen.addstr(8,        (3 + 2*xmax/3),     self.compass['Z'])
        # IR
        screen.addstr(10,       1,                  'IR Front:')
        screen.addstr(11,       1,                  'IR Rear:')
        screen.addstr(10,       (3 + xmax/3),       self.ir['FRONT'])
        screen.addstr(11,       (3 + xmax/3),       self.ir['REAR'])
        screen.refresh()
