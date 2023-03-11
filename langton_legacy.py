from langton_code import start, start_ant, time_log, count, read, read_ant, next_gen, progress_bar, render
from tkinter import Tk, Canvas, Label, Menu
from ctypes import windll

# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END

# Simulation parameters
height, width, posx, posy, pause = 100, 100, 10, 10, -1
# Correction
height += 2
width += 2
# END


def rectangle(grid, x, y, x_length, y_length, value=1):
    """
    Used to create a rectangle based on coordinates.
    Used by the place_action function, that triggers when there's a click Button-x
    """

    if x in [0, len(grid[0])]:
        x = 1
    if y in [0, len(grid)]:
        y = 1

    for xp in range(x_length):
        for yp in range(y_length):
            grid[y+yp][x+xp] = value
    return (grid)


main_grid, ant_grid, generation, number_of_generations = start(height, width), start_ant(height, width), 0, 20000
# Main grid, current generation, maximum number of generation
action, cursor_size_width, cursor_size_height = (rectangle), 1, 1


def set_action(new_action=rectangle):
    """
    Allow to change the function defined to the variable "action"
    """

    global action
    action = new_action


def set_grid():
    global main_grid, history
    window.after(func=after_loop, ms=0)


def stop_sim():
    """
    Set the simulation parameters so that it stops itself
    """

    global generation, number_of_generations
    generation = number_of_generations


def clear_grid():
    """
    Clear both grids and reset to its base state
    """

    global main_grid, ant_grid
    main_grid = start(height, width)
    ant_grid = start_ant(height, width)
    canevas.delete('all')
    update_table()

# Simulation parameters END

# Window def


window = Tk()
window.title("Game of Life")
window.configure(bg="#000000")
window.state('zoomed')

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))
# Window def END

# Menu def

window_menu = Menu(window)

file = Menu(window_menu, tearoff=0)
window_menu.add_cascade(label='File', menu=file)
file.add_command(label='Undo', command=set_grid)
file.add_separator()
file.add_command(label='Clear', command=clear_grid)
file.add_command(label='Exit', command=stop_sim)

window.config(menu=window_menu)
# Menu def END#

# [Cell State], [Turn, Cell change, Movement], [Cell color], [Rule Name]
# [Movement Behaviour: str], [Change Rule: 0,1], [Ant Color], [Rule Name]
rules = [
    ["RL", [-1,1],"#00ff00", "LANGTON ANT"]
    ]
current_rules = rules[0]


# Size determination #


def function(x):
    return (.9 * 2.718281**(-x/(2.5*2.718281)))


def size():
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    cell_size = min(int((screen_height) / (height) * function(height/100)), int((screen_width) / (width) * function(height/100)))
    font_size = int((cell_size*width/17) * function((cell_size*width)/10))
    if cell_size < 2:
        cell_size = 2
    return (cell_size, font_size)


# Size determination END #
cell = size()[0]  # Must be an integer


dimensions = ((width * (cell)), (height * (cell)))


def set_rules(id):
    global rules, current_rules
    current_rules = rules[id]


canevas = Canvas(window, bg="white", height=((height + 2) * (cell)), width=((width + 2) * (cell)))
canevas.grid(row=0, column=0)

text1 = Label(text="Test", background="#000000", fg='magenta', font=("Times New Roman", size()[1]))
text2 = Label(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__) +'    ', background="#000000", fg='#0088ff', font=("Times New Roman", size()[1]))
text3 = Label(text=progress_bar(generation, number_of_generations, mode=1)[0] + " " + str(generation) + "/" + str(number_of_generations), background="#000000", fg=progress_bar(generation, number_of_generations, mode=1)[1], font=("Times New Roman", size()[1]))
text1.grid(row=1, column=0)
text2.grid(row=2, column=0)
text3.grid(row=3, column=0)


def update_table(debug=0):
    """
    Draw all squares depending of the state of a cell
    """

    for h in range(height):
        for w in range(width):
            posx, posy = ((w + 1) * cell), ((h + 1) * cell)
            if h in [0, len(main_grid)-1] or w in [0, len(main_grid[0])-1]:
                main_grid[h][w] = -1
                canevas.create_rectangle(posx, posy, posx + cell, posy + cell, fill='#cc0000', outline='#1c1c1c')

            if read(main_grid, w, h) == 1:
                canevas.create_rectangle(posx, posy, posx + cell, posy + cell, fill="#000000")

            if read_ant(ant_grid, w, h):
                canevas.create_rectangle(posx, posy, posx + cell, posy + cell, fill=current_rules[2])


def after_loop():
    global main_grid, ant_grid, generation, number_of_generations, history
    update_table()
    text1.config(text='Generation n°%d | Rules "%s" | %sx%s | %s | Cell count: %s' % (generation, current_rules[3], dimensions[0], dimensions[1], time_log(1), count(ant_grid)))
    text2.config(text='Cursor dimensions:' + str(cursor_size_width) + 'x' + str(cursor_size_height) + ' | ' + str(action.__name__))
    text3.config(text=progress_bar(generation, number_of_generations, mode=1)[0] + " " + str(generation) + "/" + str(number_of_generations), fg=progress_bar(generation, number_of_generations, mode=1)[1])
    window.update()
    if pause == -1:
        canevas.delete('all')
        update_table()
        window.after(func=after_loop, ms=0)
    elif generation < number_of_generations:
        canevas.delete('all')
        main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height)
        generation += 1
        window.after(func=after_loop, ms=0)
    else:
        window.destroy()


def place_action(eventorigin):

    global history
    reg_x = (eventorigin.x) // cell
    reg_y = (eventorigin.y) // cell
    action(ant_grid, reg_x - 1, reg_y - 1, cursor_size_width, cursor_size_height, [1, "N"])


def destroy_cell(eventorigin):

    global history
    reg_x = (eventorigin.x) // cell
    reg_y = (eventorigin.y) // cell
    action(ant_grid, reg_x - 1, reg_y - 1, cursor_size_width, cursor_size_height, [0, "N"])


def key_press(event):
    global pause, main_grid, ant_grid, generation, current_rules, cursor_size_height, cursor_size_width
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
        print('Window forcefully closed by pressing TAB at generation n° %d at %s  ' % (generation, time_log(1)))
        stop_sim()
        pause = 1
    elif press == 'Up':
        cursor_size_height += 1
    elif press == 'Down':
        if cursor_size_height > 1:
            cursor_size_height -= 1
    elif press == 'Right':
        cursor_size_width += 1
    elif press == 'Left':
        if cursor_size_width > 1:
            cursor_size_width -= 1



# START

window.bind('<Key>', key_press)
window.bind("<B1-Motion>", place_action)
window.bind("<Button-1>", place_action)
window.bind("<B3-Motion>", destroy_cell)
window.bind("<Button-3>", destroy_cell)

update_table()
canevas.after(func=after_loop, ms=0)

window.mainloop()
