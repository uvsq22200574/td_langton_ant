from tkinter import Tk, Label, Menu, Checkbutton, IntVar, Button
from PIL import Image, ImageTk, ImageColor
from colorama import init, Fore, Style
from platform import system
init()


if operating_sytem := system() == 'Windows':
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # noqa: E501
else:
    from Xlib.display import Display
    screen = Display(':0').screen()
    screen_width, screen_height = (screen.width_in_pixels, screen.height_in_pixels)  # noqa: E501


# /=> Functions END <=/


def time_log(simple_format=False, tmp=False, tmp2=False):  # noqa: E501
    from datetime import datetime
    '''Will estimate the precise time at which it has been executed.'''
    if tmp2 is True:
        if simple_format is True:
            return ('%s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        return ('[%s]: ' % (datetime.now().strftime("%d/%m/%Y | %H:%M:%S")))
    if tmp is True:
        if simple_format is True:
            return ('%s' % (datetime.now().strftime("%H:%M:%S")))
        return ('[%s]: ' % (datetime.now().strftime("%H:%M:%S")))
    else:
        if simple_format is True:
            return ('%s' % (datetime.now().strftime("%d/%m/%Y")))
        return ('[%s]: ' % (datetime.now().strftime("%d/%m/%Y")))


def progress_bar(progress: int, total: int, init_msg='', end_msg='', tmp=0, tmp2=2):  # noqa: E501
    '''Returns or print a progress bar.'''
    percent = (progress * 100) / float(total)
    if percent % 2 == 0:
        bar = '▓' * int((percent)/tmp2) + '░' * (int((100 - percent)/tmp2))
    else:
        bar = '▓' * int((percent)/tmp2) + '░' * (int((100 - percent)/tmp2) + 1)

    if tmp == 0:
        if progress/total >= 1:
            print(Fore.GREEN + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + end_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
        elif progress/total >= .5:
            print(Fore.YELLOW + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
        else:
            print(Fore.RED + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
    else:
        if progress/total >= 1:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + end_msg + '\r', "#00FF00")  # noqa: E501
        elif progress/total >= .5:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + '\r', "#FFFF00")  # noqa: E501
        else:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + '\r', "#FF0000")  # noqa: E501


def count(table: list, tmp=1, tmp2=0):
    '''Will return the number of cells/ants of a grid.'''

    count = 0
    for y in range(len(table)):
        for x in range(len(table[0])):
            if tmp:
                count += (table[y][x][0] if table[y][x][0] > 0 else 0)
            else:
                count += (table[y][x] if table[y][x] > 0 else 0)
    percentage = ((count * 100) / ((len(table) - 2) * (len(table[0]) - 2)))
    if tmp2:
        return count
    return ('%.5d / %d (%.2f%%)' % (count, (len(table) - 2) * (len(table[0]) - 2), percentage))  # noqa: E501


def start(height, width, value=-1):
    '''Base template of a langton's cell's grid.'''

    return ([[-1 for _ in range(width)] for _ in range(height)])


def start_ant(height, width, value=[0, "N"]):
    '''Base template of a langton's ant's grid.'''

    return ([[[0, "N"] for _ in range(width)] for _ in range(height)])


def render(table: list):
    '''Print a grid in a readable way.'''

    for index in range(len(table)):
        print(*table[index], end='\n')


def case_selector(direction: str, cell_state: int, multiplier=1):
    '''Translate the direction of an ant to a grid logic.'''

    if cell_state:
        return [[0, multiplier], [-multiplier, 0], [0, -multiplier], [multiplier, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501
    return multiplier * [[0, -multiplier], [multiplier, 0], [0, multiplier], [-multiplier, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501


def interval(x: int, length_grid: int):
    '''Enable the grid to be a tor.\n /!\\ Bug: When placed at grid_length-2 * R² destroy cell'''  # noqa: E501
    if 1 <= x < length_grid-1:  # If the ant is in the grid
        return x
    elif x == 0:    # Teleport the ant to the other side
        return length_grid-2
    return (x % (length_grid-1)) + 1


def next_gen(previous_table_main: list, previous_table_ant: list, width: int, height: int, multiplier=1, steps=1):  # noqa:501
    '''
    Compute all steps, then return the next grid based on the previous one.
    '''

    new_table_main = start(len(previous_table_main), len(previous_table_main[0]))  # noqa: E501
    new_table_ant = start_ant(len(previous_table_ant), len(previous_table_ant[0]))  # noqa: E501
    angles = ["E", "N", "O", "S"]

    for x in range(1, len(previous_table_ant[0]) - 1):
        for y in range(1, len(previous_table_ant) - 1):
            # [Cell State], [Turn, Cell change, Movement], [Cell color], [Rule Name]  # noqa: E501

            # Keep drawing cells if state unchanged
            if previous_table_main[y][x] == 1:
                new_table_main[y][x] = 1

            if previous_table_ant[y][x][0]:     # If there is an ant
                if previous_table_main[y][x] == -1:     # If the cell is white
                    directions = case_selector(previous_table_ant[y][x][1], -1, multiplier)    # Select ant's new orientation  # noqa: E501
                    new_table_ant[interval(y+directions[0], height)][interval(x+directions[1], width)] = [1, angles[(angles.index(previous_table_ant[y][x][1])-1) % 4]]  # Set new ant's attributes  # noqa: E501
                else:
                    directions = case_selector(previous_table_ant[y][x][1], 1, multiplier)  # noqa: E501
                    new_table_ant[interval(y-directions[0], height)][interval(x-directions[1], width)] = [1,  angles[(angles.index(previous_table_ant[y][x][1])+1) % 4]]  # noqa: E501
                new_table_main[y][x] = -previous_table_main[y][x]   # Switch cell state  # noqa: E501

    return (new_table_main, new_table_ant)


def conv_rgb_hex(red, green, blue):
    return "#{:02x}{:02x}{:02x}".format(int(red), int(green), int(blue))


def conv_hex_rgb(color: str):
    return (ImageColor.getcolor(color, "RGB"))


def rectangle(grid, x, y, x_length, y_length, value=1):
    """
    Used to create a rectangle based on coordinates.
    Used by the place_action function, that triggers when there's a click
    """

    limit = (width-2)*(height-2)
    if x_length*y_length >= limit:
        Sim_feedback.config(text="Cannot place a full grid.", fg="#FF0000")
        return (0)
    elif (x+x_length+1 > len(grid[0])) and (y+y_length+1 > len(grid)) or (x == 0 and y == 0):  # noqa: E501
        Sim_feedback.config(text="Cannot place out of bounds in x and y axis.", fg="#FF0000")  # noqa: E501
        return (0)
    elif x+x_length+1 > len(grid[0]) or x == 0:
        Sim_feedback.config(text="Cannot place out of bounds in x axis.", fg="#FF0000")  # noqa: E501
        return (0)
    elif y+y_length+1 > len(grid) or y == 0:
        Sim_feedback.config(text="Cannot place out of bounds in y axis.", fg="#FF0000")  # noqa: E501
        return (0)
    else:
        Sim_feedback.config(text="No error reported.", fg="#00AA00")

    for xp in range(x_length):
        for yp in range(y_length):
            grid[y+yp][x+xp] = value    # y+yp means clic coordinates plus iteration  # noqa: E501


# /=> Functions END <=/


# /=> Simulation parameters <=/
height, width, posx, posy, pause = 100, 100, 10, 10, -1
height += 2; width += 2  # noqa: E702


main_grid, ant_grid = start(height, width), start_ant(height, width)

action, cursor_size_width, cursor_size_height = (rectangle), 1, 1


generation, number_of_generations, steps_per_gen, cell = 0, 20000, 1, 8
slide = 1

# [Ant Color], [Rule Name]
rules = [["#ff00ff", "#00ff00"], "LANGTON ANT"]

dimensions = ((width * (cell)), (height * (cell)))
# /=> Simulation parameters END <=/


def set_action(new_action=rectangle):
    '''
    Allow to change the function defined to the variable "action".
    For example, we can assign it to a rectangle, circle, or specific structure
    '''

    global action
    action = new_action


def stop_sim():
    '''Set the simulation parameters so that it stops itself.'''
    window.destroy()


def clear_grid():
    '''Clear both grids and reset to it's base state.'''

    global main_grid, ant_grid
    main_grid = start(height, width)
    ant_grid = start_ant(height, width)
    draw_simulation()


def fill_grid(grid=main_grid, value=-1, tmp=1):
    '''Fill both grids.'''

    for row in range(1, height-1):  # Ignore the edges, they don't need to be filled  # noqa: E501
        for column in range(1, width-1):
            if tmp:
                grid[row][column] = value
            else:
                grid[row][column] = -(grid[row][column])


# /=> Window Definition <=/


window = Tk()
window.title("Langton's Ant")
window.configure(bg="#000000")
window.state('zoomed')
window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))


# /=> Window Definition END <=/

# /=> Menu Definition <=/

window_menu = Menu(window)

File_selector = Menu(window_menu, tearoff=0)
window_menu.add_cascade(label='File', menu=File_selector)
File_selector.add_separator()
File_selector.add_command(label='Exit', command=stop_sim)


window.config(menu=window_menu)

# /=> Menu Definition END <=/


# /=> Size Determination <=/


def size():
    '''Used to determine the correct size based on the screen dimensions. WIP.'''  # noqa:501

    def function(x):
        return (.9 * 2.718281**(-x/(2.5*2.718281)))

    cell_size = min(int((screen_height) / (height) * function(height/100)), int((screen_width) / (width) * function(height/100)))  # noqa: E501
    font_size = int((cell_size*width/17) * function((cell_size*width)/10))
    if cell_size < 2:
        cell_size = 2
    return (cell_size, font_size)


# /=> Size Determination END <=/

sim_graph = Label()
sim_graph.grid(row=0, column=0, rowspan=height//2, columnspan=3)

Sim_time = Label(background="#111111", fg='#0088ff', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_date = Label(background="#111111", fg='#0088ff', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_Dimensions = Label(background="#111111", fg='#0088ff', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_stats_dimensions = Label(background="#111111", fg='#0088ff', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_feedback = Label(text="Nothing to report.", background="#111111", fg="#AAAAAA", font=("Times New Roman", size()[1]))  # noqa: E501
Sim_generation = Label(background="#111111", fg='magenta', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_cells = Label(background="#111111", fg='magenta', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_ant = Label(background="#111111", fg='magenta', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_progress = Label(background="#111111", font=("Times New Roman", size()[1]))  # noqa: E501

Sim_time.grid(row=0, column=4)
Sim_date.grid(row=1, column=4)
Sim_Dimensions.grid(row=2, column=4)
Sim_stats_dimensions.grid(row=3, column=4)
Sim_feedback.grid(row=4, column=4)
Sim_generation.grid(row=5, column=4)
Sim_cells.grid(row=6, column=4)
Sim_ant.grid(row=7, column=4)
Sim_progress.grid(row=8, column=4)


def draw_simulation():
    '''Function used for the graphic aspect of the code.'''

    images_standart_size = (width, height)
    cell_grid = Image.new("RGBA", images_standart_size, "#FFFFFF")
    pixels = cell_grid.load()
    x_sim, y_sim = ((sim_graph.winfo_pointerx()-sim_graph.winfo_rootx())//cell)*cell, ((sim_graph.winfo_pointery()-sim_graph.winfo_rooty())//cell)*cell  # noqa: E501

    for row in range(width):
        for column in range(height):
            # Draw black pixels if there's a cell.
            if main_grid[column][row] == 1:
                pixels[row, column] = (0, 0, 0)

            # Draw border's pixels if iterating at the borders.
            if (column in [0, len(main_grid)-1] or row in [0, len(main_grid[0])-1]):  # noqa: E501
                pixels[row, column] = (0, 0, 128)

            # Draw ant's pixels if there's an ant, based on if there's a cell underneath.  # noqa: E501
            if ant_grid[column][row][0] == 1:
                pixels[row, column] = conv_hex_rgb(rules[0][0]) if (main_grid[column][row] == 1) else conv_hex_rgb(rules[0][1])  # noqa: E501

    # Resize the image to be bigger.
    mid_image = ((cell_grid.resize((cell_grid.size[0] * cell, cell_grid.size[1] * cell), resample=Image.NEAREST)))  # noqa: E501

    # Draw pixels intersections as points, red if the cell is marked, black otherwise.  # noqa: E501
    pixels = mid_image.load()
    for row in range(width):
        for column in range(height):
            if not ((column in [0, len(main_grid)-1] or row in [0, len(main_grid[0])-1])):  # noqa: E501
                pixels[row*cell, column*cell] = conv_hex_rgb('#FF0000') if (main_grid[column][row] == 1 or main_grid[column-1][row-1] == 1 or main_grid[column][row-1] == 1 or main_grid[column-1][row] == 1) else conv_hex_rgb('#000000')  # noqa: E501

    if (cell <= x_sim <= dimensions[0]-cursor_size_width-1*cell and cell <= y_sim <= dimensions[1]-cursor_size_height-1*cell) and (dimensions[0] - (x_sim+(cursor_size_width)*cell) > 0) and (dimensions[1] - (y_sim+(cursor_size_height)*cell) > 0):  # noqa: E501
        for length_cursor in range(cursor_size_width*cell):
            pixels[x_sim+length_cursor, y_sim-1] = conv_hex_rgb('#FF0000')
            pixels[x_sim+length_cursor, y_sim+cursor_size_height*cell-1] = conv_hex_rgb('#FF0000')  # noqa: E501
        for height_cursor in range(cursor_size_height*cell):
            pixels[x_sim, y_sim+height_cursor-1] = conv_hex_rgb('#FF0000')
            pixels[x_sim+cursor_size_width*cell, y_sim+height_cursor-1] = conv_hex_rgb('#FF0000')  # noqa: E501

    final_image = ImageTk.PhotoImage(mid_image)
    sim_graph.configure(image=final_image)
    sim_graph.image = final_image


def after_loop():
    '''Rules to select the next behaviour of the simulation.'''

    global main_grid, ant_grid, generation, number_of_generations

    if pause == 1:
        Sim_time.config(text='Time: %s' % (time_log(True, True)))
        Sim_date.config(text='Date: %s' % (time_log(True, False, False)))
        Sim_generation.config(text="Generation: %d | Max: %d" % (generation, number_of_generations))  # noqa: E501
        Sim_cells.config(text='Cell(s): %s' % count(main_grid, 0))
        Sim_ant.config(text='Ant(s): %s' % count(ant_grid))
        Sim_progress.config(text=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[0], fg=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[1])  # noqa: E501

    if generation % 10 == 0:
        Sim_stats_dimensions.config(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__))  # noqa: E501

    window.update()
    draw_simulation()
    if pause == -1:
        draw_simulation()
        window.after(func=after_loop, ms=1)
    elif generation < number_of_generations:    # If the max number of generations has not been reached yet...  # noqa: E501
        for iteration in range(steps_per_gen):  # Number of repeats
            if steps_per_gen > 1:
                progress_bar(iteration, steps_per_gen-1)
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height, slide)  # noqa: E501
        generation += steps_per_gen
        window.after(func=after_loop, ms=1)
    else:
        window.destroy()


grid_edit = IntVar()
grid_Checkbutton = Checkbutton(bg="#444444", text="Edit Cells", variable=grid_edit)  # noqa: E501
grid_Checkbutton.grid(row=0, column=5)

Simulation_fill_white = Button(text='Fill White', command=lambda: fill_grid(main_grid, value=-1))  # noqa: E501
Simulation_fill_black = Button(text='Fill Black', command=lambda: fill_grid(main_grid, value=1))  # noqa: E501
Simulation_reverse = Button(text='Invert White/Black', command=lambda: fill_grid(main_grid, tmp=0))  # noqa: E501
Simulation_clear = Button(text='Clear', command=lambda: clear_grid())
Simulation_fill_white.grid(row=1, column=5)
Simulation_fill_black.grid(row=2, column=5)
Simulation_reverse.grid(row=3, column=5)
Simulation_clear.grid(row=4, column=5)


def place_action(eventorigin):
    '''Action of creating a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [1, "N"]), (main_grid, 1)][int(grid_edit.get())]  # noqa: E501
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])  # noqa: E501

    Sim_cells.config(text='Cell(s): %s' % count(main_grid, 0))
    Sim_ant.config(text='Ant(s): %s' % count(ant_grid))


def destroy_cell(eventorigin):
    '''Action of destroying a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [0, "N"]), (main_grid, -1)][int(grid_edit.get())]  # noqa: E501
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])  # noqa: E501

    Sim_cells.config(text='Cell(s): %s' % count(main_grid, 0))
    Sim_ant.config(text='Ant(s): %s' % count(ant_grid))


def key_press(event):
    '''Assign actions to keyboard key.'''
    global pause, main_grid, ant_grid, generation, cursor_size_height, cursor_size_width  # noqa: E501

    Sim_Dimensions.config(text='Dimensions: %dx%d' % dimensions)
    press = event.keysym
    if press == 'space':
        pause = -(pause)    # Toggle the pause state
    elif press == 'f':
        Sim_time.config(text='Time: %s' % (time_log(True, True)))
        Sim_date.config(text='Date: %s' % (time_log(True, False, False)))
        Sim_generation.config(text="Generation: %d | Max: %d" % (generation, number_of_generations))  # noqa: E501
        Sim_cells.config(text='Cell(s): %s' % count(main_grid, 0))
        Sim_ant.config(text='Ant(s): %s' % count(ant_grid))
        Sim_stats_dimensions.config(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__))  # noqa: E501
        Sim_progress.config(text=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[0], fg=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[1])  # noqa: E501

        if pause == 1:  # If not paused, then pause the simulation
            pause = -(pause)
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height, slide)  # noqa: E501
            generation += 1
        else:
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height, slide)  # noqa: E501
            generation += 1
    elif press == 'Tab':
        print('Attempted a forced window closure by pressing TAB at generation n° %d at %s  ' % (generation, time_log(True)))  # noqa: E501
        pause = 1
        stop_sim()
    elif press == 'Up':
        if cursor_size_height < height-2:   # If size limit not reached
            cursor_size_height += 1
    elif press == 'Down':
        if 1 < cursor_size_height:  # If size bigger than 1
            cursor_size_height -= 1
    elif press == 'Right':
        if cursor_size_width < width-2:  # If size limit not reached
            cursor_size_width += 1
    elif press == 'Left':
        if 1 < cursor_size_width:   # If size bigger than 1
            cursor_size_width -= 1


# /=> Start <=/

window.bind('<Key>', key_press)
sim_graph.bind("<B1-Motion>", place_action)
sim_graph.bind("<Button-1>", place_action)
sim_graph.bind("<B3-Motion>", destroy_cell)
sim_graph.bind("<Button-3>", destroy_cell)

window.after(func=after_loop, ms=0)


window.mainloop()
