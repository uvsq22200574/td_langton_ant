from langton_code import start, start_ant, time_log, count, next_gen, progress_bar  # noqa: E501
from tkinter import Tk, Label, Menu, Checkbutton, IntVar, Button
from PIL import Image, ImageTk
from ctypes import windll   # Seems to not work on linux systems

# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END


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
            grid[y+yp][x+xp] = value


# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END

# Simulation parameters
height, width, posx, posy, pause = 100, 100, 10, 10, -1
# Dimensions correction (Border)
height += 2
width += 2

main_grid, ant_grid = start(height, width), start_ant(height, width)

action, cursor_size_width, cursor_size_height = (rectangle), 1, 1


screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # noqa: E501
generation, number_of_generations, steps_per_gen, cell = 0, 20000, 1, 10

# [Movement Behaviour: str], [Change Rule: 0,1], [Ant Color], [Rule Name]
rules = [["#00ff00", "#ff00ff"], "LANGTON ANT"]

dimensions = ((width * (cell)), (height * (cell)))
# END


def set_action(new_action=rectangle):
    '''Allow to change the function defined to the variable "action".'''

    global action
    action = new_action


def stop_sim():
    '''Set the simulation parameters so that it stops itself.'''

    global generation, number_of_generations, pause
    generation = number_of_generations
    pause = 1


def clear_grid():
    '''Clear both grids and reset to it's base state.'''

    global main_grid, ant_grid
    main_grid = start(height, width)
    ant_grid = start_ant(height, width)
    draw_simulation()


def fill_grid(grid=main_grid, value=-1, tmp=1):
    '''Fill both grids.'''

    for row in range(1, height-1):
        for column in range(1, width-1):
            if tmp:
                grid[row][column] = value
            else:
                grid[row][column] = -(grid[row][column])

# Simulation parameters END

# Window def


window = Tk()
window.title("Langton's Ant")
window.configure(bg="#000000")
window.state('zoomed')
window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))


# Window def END

# Menu def

window_menu = Menu(window)

File_selector = Menu(window_menu, tearoff=0)
window_menu.add_cascade(label='File', menu=File_selector)
File_selector.add_separator()
File_selector.add_command(label='Exit', command=stop_sim)


window.config(menu=window_menu)
# Menu def END#

# Size determination #


def size():
    '''Used to determine the correct size based on the screen dimensions. WIP.'''  # noqa:501

    def function(x):
        return (.9 * 2.718281**(-x/(2.5*2.718281)))

    cell_size = min(int((screen_height) / (height) * function(height/100)), int((screen_width) / (width) * function(height/100)))  # noqa: E501
    font_size = int((cell_size*width/17) * function((cell_size*width)/10))
    if cell_size < 2:
        cell_size = 2
    return (cell_size, font_size)


# Size determination END #

sim_graph = Label()
sim_graph.grid(row=0, column=0)

Sim_stats_1 = Label(text="", background="#000000", fg='magenta', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_stats_2 = Label(text="", background="#000000", fg='magenta', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_parameters_1 = Label(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__) + '    ', background="#000000", fg='#0088ff', font=("Times New Roman", size()[1]))  # noqa: E501
Sim_progress = Label(text=progress_bar(generation, number_of_generations, tmp=1)[0] + " " + str(generation) + "/" + str(number_of_generations), background="#000000", fg=progress_bar(generation, number_of_generations, tmp=1)[1], font=("Times New Roman", size()[1]))  # noqa: E501
Sim_feedback = Label(text="Nothing to report.", background="#000000", fg="#AAAAAA", font=("Times New Roman", size()[1]))  # noqa: E501
Sim_stats_1.grid(row=1, column=0)
Sim_stats_2.grid(row=2, column=0)
Sim_parameters_1.grid(row=3, column=0)
Sim_progress.grid(row=4, column=0)
Sim_feedback.grid(row=5, column=0)


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
                pixels[row, column] = (255, 0, 255) if (main_grid[column][row] == 1) else (0, 255, 0)  # noqa: E501

    # Resize the image to be bigger.
    mid_image = ((cell_grid.resize((cell_grid.size[0] * cell, cell_grid.size[1] * cell), Image.Resampling.NEAREST)))  # noqa: E501

    # Draw pixels intersections as points, red if the cell is marked, black otherwise.  # noqa: E501
    pixels = mid_image.load()
    for row in range(width):
        for column in range(height):
            if not ((column in [0, len(main_grid)-1] or row in [0, len(main_grid[0])-1])):  # noqa: E501
                pixels[row*cell, column*cell] = (255, 0, 0) if (main_grid[column][row] == 1 or main_grid[column-1][row-1] == 1 or main_grid[column][row-1] == 1 or main_grid[column-1][row] == 1) else (0, 0, 0)  # noqa: E501

    if (cell <= x_sim <= dimensions[0]-cursor_size_width-1*cell and cell <= y_sim <= dimensions[1]-cursor_size_height-1*cell) and (dimensions[0] - (x_sim+(cursor_size_width)*cell) > 0) and (dimensions[1] - (y_sim+(cursor_size_height)*cell) > 0):  # noqa: E501
        for length_cursor in range(cursor_size_width*cell):
            pixels[x_sim+length_cursor, y_sim-1] = (255, 0, 0)
            pixels[x_sim+length_cursor, y_sim+cursor_size_height*cell-1] = (255, 0, 0)  # noqa: E501
        for height_cursor in range(cursor_size_height*cell):
            pixels[x_sim, y_sim+height_cursor-1] = (255, 0, 0)
            pixels[x_sim+cursor_size_width*cell, y_sim+height_cursor-1] = (255, 0, 0)  # noqa: E501

    final_image = ImageTk.PhotoImage(mid_image)
    sim_graph.configure(image=final_image)
    sim_graph.image = final_image


def after_loop():
    '''Rules to select the next behaviour of the simulation.'''

    global main_grid, ant_grid, generation, number_of_generations

    Sim_stats_1.config(text='Generation n°%d | Rules "%s" | %sx%s | %s' % (generation, rules[1], dimensions[0], dimensions[1], time_log(1)))  # noqa: E501
    Sim_stats_2.config(text='Cell count: %s | Ant count: %s' % (count(main_grid, 0), count(ant_grid)))  # noqa: E501
    Sim_parameters_1.config(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__))  # noqa: E501
    Sim_progress.config(text=progress_bar(generation, number_of_generations, tmp=1)[0] + " " + str(generation) + "/" + str(number_of_generations), fg=progress_bar(generation, number_of_generations, tmp=1)[1])  # noqa: E501
    window.update()
    draw_simulation()
    if pause == -1:
        draw_simulation()
        window.after(func=after_loop, ms=1)
    elif generation < number_of_generations:
        for iteration in range(steps_per_gen):
            if steps_per_gen > 1:
                progress_bar(iteration, steps_per_gen-1)
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height)
        generation += steps_per_gen
        window.after(func=after_loop, ms=1)
    else:
        window.destroy()


grid_edit = IntVar()
grid_Checkbutton = Checkbutton(bg="#AAAAAA", text="Edit Cells", variable=grid_edit)  # noqa: E501
grid_Checkbutton.place(x=1200, y=100)

Simulation_fill_white = Button(text='Fill White', command=lambda: fill_grid(main_grid, value=-1))  # noqa: E501
Simulation_fill_black = Button(text='Fill Black', command=lambda: fill_grid(main_grid, value=1))  # noqa: E501
Simulation_reverse = Button(text='Invert White/Black', command=lambda: fill_grid(main_grid, tmp=0))  # noqa: E501
Simulation_clear = Button(text='Clear', command=lambda: clear_grid())
Simulation_fill_white.place(x=1200, y=200)
Simulation_fill_black.place(x=1200, y=300)
Simulation_reverse.place(x=1200, y=400)
Simulation_clear.place(x=1200, y=500)


def place_action(eventorigin):
    '''Action of creating a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [1, "N"]), (main_grid, 1)][int(grid_edit.get())]  # noqa: E501
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])  # noqa: E501


def destroy_cell(eventorigin):
    '''Action of destroying a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [0, "N"]), (main_grid, -1)][int(grid_edit.get())]  # noqa: E501
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])  # noqa: E501


def key_press(event):
    '''Assign actions to keyboard key.'''
    global pause, main_grid, ant_grid, generation, cursor_size_height, cursor_size_width  # noqa: E501

    press = event.keysym
    if press == 'space':
        pause = -(pause)
    elif press == 'f':
        if pause == 1:
            pause = -(pause)
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height)
            generation += 1
        else:
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height)
            generation += 1
    elif press == 'Tab':
        print('Attempted a forced window closure by pressing TAB at generation n° %d at %s  ' % (generation, time_log(1)))  # noqa: E501
        stop_sim()
        pause = 1
    elif press == 'Up':
        if cursor_size_height < height-2:
            cursor_size_height += 1
    elif press == 'Down':
        if 1 < cursor_size_height:
            cursor_size_height -= 1
    elif press == 'Right':
        if cursor_size_width < width-2:
            cursor_size_width += 1
    elif press == 'Left':
        if 1 < cursor_size_width:
            cursor_size_width -= 1


# START

window.bind('<Key>', key_press)
sim_graph.bind("<B1-Motion>", place_action)
sim_graph.bind("<Button-1>", place_action)
sim_graph.bind("<B3-Motion>", destroy_cell)
sim_graph.bind("<Button-3>", destroy_cell)

window.after(func=after_loop, ms=0)


window.mainloop()
