import serial
import matplotlib


class rover(object):
    def __init__(self):
        self.address = '/dev/tty.usbserial-AJV9OOBQ'
        self.ir = {'FRONT': 0, 'REAR': 0}
        self.accel = {'X': 0, 'Y': 0, 'Z': 0}
        self.gyro = {'X': 0, 'Y': 0, 'Z': 0}
        self.compass = {'X': 0, 'Y': 0, 'Z': 0}
        self.pose = {'X': 0, 'Y': 0, 'Z': 0}

    def connect(self):
        self.serial = serial.Serial('/dev/tty.usbserial-AJV9OOBQ', 38400)

    def read(self):
        print(self.serial.readline())
        # probably have to send a request to read. think about this
