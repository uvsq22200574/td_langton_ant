from tkinter import Tk, Canvas, Label, Menu
from ctypes import windll
from time import time
from colorama import init, Fore, Style
from datetime import datetime
from PIL import Image, ImageTk

init()

# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END

# Functions

# Utility


def func_name():
    ''' Allows to identify the exact function. Use as a string variable.'''
    from traceback import extract_stack
    return (__name__ + '(' + extract_stack(None, 2)[0][2]) + ')'


def time_log(simple_format=0):  # Will estimate the precise time at which it has been executed
    if simple_format == 1:
        return ('%s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    return ('[%s]: ' % (datetime.now().strftime("%d/%m/%Y | %H:%M:%S")))


def progress_bar(progress, total, init_msg='', end_msg='', mode=0):
    percent, time = (progress * 100) / float(total), time_log(1)
    if percent % 2 == 0:
        bar = '▓' * int((percent)/2) + '░' * (int((100 - percent)/2))
    else:
        bar = '▓' * int((percent)/2) + '░' * (int((100 - percent)/2) + 1)

    if mode == 0:
        if progress/total >= 1:
            print(Fore.GREEN + '╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + end_msg + Style.RESET_ALL, sep=' ', end='\n')
        elif progress/total >= .5:
            print(Fore.YELLOW + '╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')
        else:
            print(Fore.RED + '╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')
    else:
        if progress/total >= 1:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + end_msg + '\r', "#00FF00")
        elif progress/total >= .5:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + init_msg + '\r', "#FFFF00")
        else:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, time) + ' ' + init_msg + '\r', "#FF0000")

# Utility END
def start(height: int, width: int):
    '''Will generate the base grid that contains the cells.'''
    return ([[-1 for _ in range(width)] for _ in range(height)])


def start_ant(height: int, width: int):
    '''Will generate the base grid that contains the ants.'''
    return ([[[0, "N"] for _ in range(width)] for _ in range(height)])


def read(table: list, x: int, y: int):
    ''' Returns the value based on coordinates. Made for the cell's grid.'''
    return (table[y][x])


def read_ant(table: list, x: int, y: int, mode=1):
    '''
    Returns the value based on coordinates. Made for the ant's grid.\n
    Possibility to return either the existence of an ant or the orientation.\n
    The default ant value is 0 (No Ant) and orientation is "N" (North).\n
    Orientation is independant of an Ant.
    '''
    if mode:
        return (table[y][x][0])
    return (table[y][x][1])


def rectangle(grid: list, x: int, y: int, x_length: int, y_length: int, value=1):
    '''
    Used to create a rectangle based on coordinates.\n
    Used by the place_action function, that triggers when there's a click.
    '''

    if x in [0, len(grid[0])]:
        x = 1
    if y in [0, len(grid)]:
        y = 1

    for xp in range(x_length):
        for yp in range(y_length):
            grid[y+yp][x+xp] = value
    return (grid)


def clear_grid():
    '''Clear both grids and reset to its base state.'''

    global main_grid, ant_grid
    main_grid = start(height, width)
    ant_grid = start_ant(height, width)
    print("From %s: Missing Draw Simulation" % func_name())

# END

# Simulation parameters/variables


height, width, posx, posy, pause = 101, 101, 10, 10, -1

main_grid, ant_grid = start(height, width), start_ant(height, width)

action, cursor_size_width, cursor_size_height = (rectangle), 1, 1

generation, number_of_generations, steps_per_gen = 0, 20000, 25

cell_size = 8

screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# [Ant Colors], [Rule Name]
rules = [["#00ff00", "#ff00ff"], "LANGTON ANT"]

dimensions = ((width * (cell_size)), (height * (cell_size)))
# Correction

height += 2
width += 2

# END

# Window definition


window = Tk()
window.title("Langton's Ant")
window.configure(bg="#000000")
window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))
window.state('zoomed')

# Window def END


canevas = Canvas(window, bg="white", height=((height + 2) * (cell_size)), width=((width + 2) * (cell_size)))
canevas.grid(row=0, column=0)


if __name__ == "__main__":
    pass


window.mainloop()
