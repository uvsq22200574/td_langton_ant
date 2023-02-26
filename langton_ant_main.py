from tkinter import Tk, Canvas, Label, Menu
from ctypes import windll
from time import time
from colorama import init, Fore, Style
from datetime import datetime

init()

# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END

# Functions


def start(height: int, width: int):
    '''Will generate the base grid that contains the cells.'''
    return ([[-1 for _ in range(width)] for _ in range(height)])


def start_ant(height: int, width: int):
    '''Will generate the base grid that contains the ants.'''
    return ([[[0, "N"] for _ in range(width)] for _ in range(height)])


def rectangle(grid: list, x: int, y: int, x_length: int, y_length: int, value=1):
    '''
    Used to create a rectangle based on coordinates.
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

# END

# Simulation parameters/variables


height, width, posx, posy, pause = 101, 101, 10, 10, -1

main_grid, ant_grid = start(height, width), start_ant(height, width)

action, cursor_size_width, cursor_size_height = (rectangle), 1, 1

generation, number_of_generations, steps_per_gen = 0, 20000, 25

cell_size = 8

screen_width, screen_height = user32.GetSystemMetrics

# [Ant Colors], [Rule Name]
rules = [["#00ff00", "#ff00ff"], "LANGTON ANT"]

dimensions = ((width * (cell_size)), (height * (cell_size)))
# Correction

height += 2
width += 2

# END


window = Tk()
window.title("Langton's Ant")
window.configure(bg="#000000")
window.state('zoomed')


window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))
# Window def END


canevas = Canvas(window, bg="white", height=((height + 2) * (cell_size)), width=((width + 2) * (cell_size)))
canevas.grid(row=0, column=0)


window.mainloop()
