#!/usr/bin/python
import curses
from time import sleep
from rover import Rover
import plotly.plotly as py
from collections import deque


def main(screen):
    # INIT CURSES LAYOUT COMPONENTS
    curses.use_default_colors()
    curses.curs_set(0)
    screen.nodelay(True)
    ymax, xmax = screen.getmaxyx()
    clear = [' '] * (xmax - 1)
    delimiter = ['-'] * len(clear)
    clear = ''.join(clear)
    delimiter = ''.join(delimiter)
    # CONSOLE DEQUE
    console = deque(maxlen=5)
    console.appendleft('Hello, World!')
    # CONTROL VARS
    toggle_plot = False
    plot_accel = False
    plot_gyro = False
    plot_compass = False
    # CONNECT TO ROVER
    my_rover = Rover('/dev/tty.usbserial-AJV9OOBQ')
    screen.addstr(1, 1, 'ROVER1', curses.A_STANDOUT)
    screen.addstr(1, 7, ' connecting to ' + my_rover.address, curses.A_DIM)
    screen.refresh()
    my_rover.connect()
    if my_rover.connected is True:
        screen.addstr(1, 7, ' connected on ' + my_rover.address, curses.A_DIM)
        screen.addstr(1, (xmax - 7), '[q]uit')
        screen.addstr(2, 1, delimiter)

        screen.addstr(ymax-2, 1, delimiter)
        screen.addstr((ymax-1), 1, '[p]lot data')
        screen.addstr((ymax-1), xmax/4, '[m]anual mode')
        screen.refresh()
    else:
        print("Connection Failed")
        exit()
    while my_rover.connected is True:
        # CONTROL ROVER
        my_rover.read()
        _ = my_rover.log2curses(screen)
        if plot_accel is True:
            my_rover.plot_accel()
            if not(my_rover.accel_plot.plotly_address in console):
                console.appendleft(my_rover.accel_plot.plotly_address)
        if plot_gyro is True:
            my_rover.plot_gyro()
            if not(my_rover.gyro_plot.plotly_address in console):
                console.appendleft(my_rover.gyro_plot.plotly_address)
        if plot_compass is True:
            my_rover.plot_compass()
            if not(my_rover.compass_plot.plotly_address in console):
                console.appendleft(my_rover.compass_plot.plotly_address)
        # READ FROM USER
        user_input = screen.getch()
        # MENU ACTIONS
        if user_input == ord('q'):
            exit()
        if user_input == ord('p'):
            console.appendleft('Select data to plot: [1] Accelerometer, [2] Gyroscope, [3] Compass')
            console.appendleft('Plotting data significant increases delta t. Press [p] to cancel')
            toggle_plot = not(toggle_plot)
        if user_input == ord('1') and toggle_plot is True:
            console.appendleft('Plotting Accelerometer Data')
            plot_accel = True
            toggle_plot = False
        if user_input == ord('2') and toggle_plot is True:
            console.appendleft('Plotting Gyro Data')
            plot_gyro = True
            toggle_plot = False
        if user_input == ord('3') and toggle_plot is True:
            console.appendleft('Plotting Compass Data')
            plot_compass = True
            toggle_plot = False
        if user_input == ord('m'):
            console.appendleft('Manual Mode using WASD keypad')
        # UPDATE CONSOLE
        for i, message in enumerate(console):
            screen.addstr((ymax - (i + 3)), 1, clear)
            screen.addstr((ymax - (i + 3)), 1, message)


curses.wrapper(main)
