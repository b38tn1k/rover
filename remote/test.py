from rover import rover
from time import sleep
# START ROVER
my_rover = rover('/dev/tty.usbserial-AJV9OOBQ')
print('CONNECTING...')
my_rover.initialize_plotly()
my_rover.connect()
if my_rover.connected is True:
    print('SUCCESS!')
while True:
    my_rover.read()
    # my_rover.log2cli()
    sleep(0.2)
    my_rover.update_plotly()
