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
    clear = ''.join([' '] * (xmax - 1))
    delimiter = ''.join(['_'] * (xmax - 1))
    # CONSOLE DEQUE
    console = deque(maxlen=25)
    console.appendleft('Hello, World!')
    # CONTROL VARS
    toggle_plot = False
    plot_accel = False
    plot_gyro = False
    plot_compass = False
    wasd_mode = False
    speed = 20
    turning_ratio = 0.7
    # CONNECT TO ROVER
    my_rover = Rover('/dev/tty.usbserial-AJV9OOBQ')
    screen.addstr(1, 1, 'ROVER1', curses.A_STANDOUT)
    screen.addstr(1, 7, ' connecting to ' + my_rover.address, curses.A_DIM)
    screen.addstr(3, 1, 'DO NOT ADJUST YOUR TERMINAL', curses.A_BLINK)
    screen.addstr(4, 1, 'YOU WILL BREAK SOMETHING', curses.A_BLINK)
    screen.refresh()
    my_rover.connect()
    if my_rover.connected is True:
        screen.clear()
        screen.addstr(1, 1, 'ROVER1', curses.A_STANDOUT)
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
        # UPDATE CONSOLE
        for i, message in enumerate(console):
            screen.addstr((ymax - (i + 3)), 1, clear)
            screen.addstr((ymax - (i + 3)), 1, message)
        # READ FROM USER
        user_input = screen.getch()
        # MENU ACTIONS
        if user_input == ord('q'):
            if wasd_mode is False:
                exit()
            else:
                console.appendleft('Exit Manual Mode to Quit')
        if user_input == ord('p'):
            toggle_plot = not(toggle_plot)
            if toggle_plot is True:
                console.appendleft('Select data to plot: [1] Accelerometer, [2] Gyroscope, [3] Compass')
                console.appendleft('Plotting data significant increases delta t.')
                console.appendleft('Press [p] to cancel')
            else:
                console.appendleft('Plotting cancelled')
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
            wasd_mode = not(wasd_mode)
            if wasd_mode is True:
                console.appendleft('Manual Mode using WASD keypad')
                console.appendleft('Default Values:')
                console.appendleft('Speed:\t\t{} with range 0:100'.format(speed))
                console.appendleft('Turning Ratio:\t{} with range 0:1'.format(turning_ratio))
                console.appendleft('Primary Controls:')
                console.appendleft('w:\t\tForwards')
                console.appendleft('a:\t\tBackwards')
                console.appendleft('s:\t\tRatio Turn Left')
                console.appendleft('d:\t\tRatio Turn Right')
                console.appendleft('q:\t\t0 Turn Left')
                console.appendleft('e:\t\t0 Turn Right')
                console.appendleft('SPACE:\t\tBrake!')
                console.appendleft('Secondary Controls:')
                console.appendleft('SHIFT for +10 else +1:')
                console.appendleft('x:\t\tIncrease Speed')
                console.appendleft('z:\t\tDecrease Speed')
                console.appendleft('r:\t\tIncrease Turn Ratio')
                console.appendleft('t:\t\tDecrease Turn Ratio')
                console.appendleft('Press [m] to cancel')
            else:
                console.appendleft('Manual Mode cancelled')
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
        screen.refresh()


curses.wrapper(main)
