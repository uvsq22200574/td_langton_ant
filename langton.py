from tkinter import Tk, Label, Checkbutton, IntVar, Button, simpledialog, PhotoImage, LabelFrame
from PIL import Image, ImageTk
from colorama import Fore, Style
from platform import system
from os import path, listdir, mkdir, chdir
from uuid import uuid4
from json import dumps, load
from time import time
from datetime import datetime


"""
Better with a font with ligatures, you can download 'Fira Code' at this link:
Font Page: https://github.com/tonsky/FiraCode
Direct Download: https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip
Do not forget to configure VS Code to use that font and enable ligatures.

This programm requires to have libraries not pre-installed: Pillow ; colorama.
To install libraries, open a terminal and write " pip install {library1 library2 libraryx} ".
"""

# /=> System Compatibility <=/
chdir(path.dirname(path.realpath(__file__)))

# Set current file path in the variable
ROOT_DIR = path.dirname(path.abspath(__file__))
operating_system = system()
if operating_system == 'Windows':
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    windowState = "zoomed"
    print(Fore.GREEN + "Sucessfully determined operating system. You are running on '%s' with display dimensions '%dx%d' and window state as '%s'." % (operating_system, screen_width, screen_height, windowState) + Style.RESET_ALL, sep='')
elif operating_system == 'Linux':
    from Xlib.display import Display
    screen = Display(':0').screen()
    screen_width = screen.width_in_pixels
    screen_height = screen.height_in_pixels
    windowState = "normal"
    print(Fore.GREEN + "Sucessfully determined operating system. You are running on '%s' with display dimensions '%dx%d' and window state as '%s'." % (operating_system, screen_width, screen_height, windowState) + Style.RESET_ALL, sep='')
else:
    raise Exception(Fore.RED + "Could not determine the operating system." + Style.RESET_ALL)


# /=> System Compatibility END <=/

# /=> Dependancies <=/


def time_log(simple_format=False, tmp=False, tmp2=False):
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


def progress_bar(progress: int, total: int, init_msg='', end_msg='', tmp=0, tmp2=2):
    '''Returns or print a progress bar.'''
    percent = (progress * 100) / float(total)
    if percent % 2 == 0:
        bar = '▓' * int((percent) / tmp2) + '░' * (int((100 - percent) / tmp2))
    else:
        bar = '▓' * int((percent) / tmp2) + '░' * (int((100 - percent) / tmp2) + 1)

    if tmp == 0:
        if progress / total >= 1:
            print(Fore.GREEN + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + end_msg + Style.RESET_ALL, sep=' ', end='\r')
        elif progress / total >= .5:
            print(Fore.YELLOW + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')
        else:
            print(Fore.RED + '╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')
    else:
        if progress / total >= 1:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + end_msg + '\r', "#00FF00")
        elif progress / total >= .5:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + '\r', "#FFFF00")
        else:
            return ('╠%s╣ %.3f %%' % (bar, percent) + ' ' + init_msg + '\r', "#FF0000")


def count(table: list, tmp=1, tmp2=0):
    '''Will return the number of cells/ants of a grid.'''

    count = 0
    for row in range(len(table)):
        for column in range(len(table[0])):
            if tmp:
                count += (table[row][column][0] if table[row][column][0] > 0 else 0)
            else:
                count += (table[row][column] if table[row][column] > 0 else 0)
    percentage = ((count * 100) / ((len(table) - 2) * (len(table[0]) - 2)))
    if tmp2:
        return (count)
    return "%.5d / %.5d (%.3f%%)" % (count, (len(table) - 2) * (len(table[0]) - 2), percentage)


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

    if cell_state:  # If there a black cell, use set of rules, else use inverse
        return [[0, multiplier], [-multiplier, 0], [0, -multiplier], [multiplier, 0]][["E", "N", "O", "S"].index(direction)]
    return [[0, -multiplier], [multiplier, 0], [0, multiplier], [-multiplier, 0]][["E", "N", "O", "S"].index(direction)]


def case_selector_reverse(direction: str, multiplier=1):
    '''same but for the previous_gen function'''

    return [[-multiplier, 0], [0, -multiplier], [multiplier, 0], [0, multiplier]][["E", "N", "O", "S"].index(direction)]


def interval(coord: int, length_grid: int):
    '''Enable the grid to be a tor.\n /!\\ Bug: When placed at grid_length-slide * R² it destroy the cell.'''
    if 1 <= coord < length_grid - 1:  # If the ant is in the grid
        return (coord)
    elif coord == 0:    # Teleport the ant to the other side
        return (length_grid - 2)
    elif length_grid - coord - 1 == slide:
        return (coord % (length_grid - 1) + 1)
    return (coord % (length_grid - 1) + 1)


def conv_hex_rgb(color: str):
    return (int(color[1:-4], 16), int(color[3:-2], 16), int(color[5:], 16))


def next_gen(previous_table_main: list, previous_table_ant: list, width: int, height: int, multiplier=1, steps_per_cycle=1):
    '''
    Compute all steps, then return the next grid based on the previous one.
    '''
    new_table_main = start(len(previous_table_main), len(previous_table_main[0]))
    new_table_ant = start_ant(len(previous_table_ant), len(previous_table_ant[0]))
    angles = ["E", "N", "O", "S"]

    for x in range(1, len(previous_table_ant[0]) - 1):
        for y in range(1, len(previous_table_ant) - 1):
            # Keep drawing cells if state unchanged
            if previous_table_main[y][x] == 1:
                new_table_main[y][x] = 1

            if previous_table_ant[y][x][0]:  # If there is an ant
                if previous_table_main[y][x] == -1:  # If the cell is white
                    directions = case_selector(previous_table_ant[y][x][1], -1, multiplier)    # Select ant's new orientation
                    new_table_ant[interval(y + directions[0], height)][interval(x + directions[1], width)] = [1, angles[(angles.index(previous_table_ant[y][x][1]) - 1) % 4]]  # Set new ant's attributes
                else:   # If the cell is black
                    directions = case_selector(previous_table_ant[y][x][1], 1, multiplier)
                    new_table_ant[interval(y - directions[0], height)][interval(x - directions[1], width)] = [1, angles[(angles.index(previous_table_ant[y][x][1]) + 1) % 4]]
                new_table_main[y][x] = -previous_table_main[y][x]   # Switch cell state
    return (new_table_main, new_table_ant)


def previous_gen(current_table_main: list, current_table_ant: list, width: int, height: int, multiplier=1, steps_per_cycle=1):
    '''
    the same as next_gen but the ants go backwards
    press 'd' to use.
    '''

    new_table_main = start(len(current_table_main), len(current_table_main[0]))
    new_table_ant = start_ant(len(current_table_ant), len(current_table_ant[0]))
    angles = ["E", "N", "O", "S"]

    for x in range(1, len(current_table_ant[0]) - 1):
        for y in range(1, len(current_table_ant) - 1):

            # Keep drawing cells if state unchanged
            if current_table_main[y][x] == 1:
                new_table_main[y][x] = 1

            if current_table_ant[y][x][0]:  # If there is an ant
                directions = case_selector_reverse(current_table_ant[y][x][1], multiplier)  # 'takes a step back'
                if current_table_main[interval(y + directions[0], height)][interval(x + directions[1], width)] == -1:
                    new_table_ant[interval(y - directions[0], height)][interval(x - directions[1], width)] = [1, angles[(angles.index(current_table_ant[y][x][1]) - 1) % 4]]  # Set new ant's attributes
                    new_table_main[interval(y - directions[0], height)][interval(x - directions[1], width)] = -current_table_main[interval(y - directions[0], height)][interval(x - directions[1], width)]  # Switch cell state
                else:
                    new_table_ant[interval(y + directions[0], height)][interval(x + directions[1], width)] = [1, angles[(angles.index(current_table_ant[y][x][1]) + 1) % 4]]
                    new_table_main[interval(y + directions[0], height)][interval(x + directions[1], width)] = -current_table_main[interval(y + directions[0], height)][interval(x + directions[1], width)]

    return (new_table_main, new_table_ant)


# /=> Save functions <=/


def save(state: dict) -> None:
    """
    save simulation's state
    :state:dict an object containing the variables (main_grid, ant_grid, width, height)
    :return: None
    """
    saves = listSaves()
    save_selection_window = Tk()
    save_selection_window.title('Select a save file or create a new one:')

    # Set the geometry
    save_selection_window.geometry("600x600")
    save_selection_window.eval('tk::PlaceWindow . center')
    save_selection_window.resizable(False, False)

    # If there is no save, add a label
    if len(saves) == 0:
        emptyLabel = Label(save_selection_window, text="No saves for now", anchor='center')
        emptyLabel.pack(pady=10)
    # If there is saves, list them to allow update
    else:
        for iteration, iterated_save_file in enumerate(saves):
            save = iterated_save_file
            saveLabel = Label(save_selection_window, text=save['saveName'], anchor="w", cursor="hand2")
            saveLabel.pack()
            saveLabel.bind("<Button-1>", lambda event, save=save: updateEntry(state, save, save_selection_window))
            saveDate = datetime.fromtimestamp(save['createdAt'])
            saveUpdate = datetime.fromtimestamp(save['updatedAt'])
            saveInfo = "Created at : " + saveDate.strftime("%d/%m/%Y, %H:%M:%S") + " - Last update : " + saveUpdate.strftime("%d/%m/%Y, %H:%M:%S")
            dateLabel = Label(save_selection_window, text=saveInfo, anchor="w", font=("Times New Roman", 8))
            dateLabel.pack()

    newSaveButton = Button(save_selection_window, text="New save", command=lambda: newEntry(state, save_selection_window))
    newSaveButton.pack(pady=50)

    save_selection_window.mainloop()


# Update an existing entry
def updateEntry(state: dict, save: dict, window: Tk) -> None:
    """
    Update a save entry
    :state:dict an object containing the variables(main_grid, ant_grid, width, height)
    :save: dict an object containing the dates, id and name of the save entry
    :window: a window tkinter
    :return:None
    """
    entry = {
        "state": state,
        "saveName": save['saveName'],
        "id": save['id'],
        "createdAt": save['createdAt'],
        "updatedAt": time()
    }
    saveEntry(entry)
    window.destroy()
    pass


# create a new entry
def newEntry(state: dict, window: Tk) -> None:
    """
    Create a new entry for the save
    :state:dict an object containing the variables(main_grid, ant_grid, width, height)
    :window: a window tkinter
    :return: None
    """
    name = simpledialog.askstring("Choose a name", "Name :")
    time_v = time()
    entry = {
        "saveName": name,
        "id": str(uuid4()),
        "createdAt": time_v,
        "updatedAt": time_v,
        "state": state
    }
    saveEntry(entry)
    window.destroy()


# Add content to file
def saveEntry(entry: dict) -> None:
    """
    Write "entry" to file
    :entry: dict an object containing the variables(state, saveName, id, createdAt, updateAt)
    :return: None
    """

    # Make sure save directory exists
    filepath = _getFile('{%s}_%s' % (entry['saveName'], entry['id']))
    # Open file and write to it
    handler = open(filepath, 'w+')
    handler.write(dumps(entry))
    handler.close()


# List all saves
def listSaves() -> None:
    """
    Create a list of all saves
    :return: None
    """
    saves = []
    _ensureSaveDirectoryExists()
    directory = _getSaveDirectoryPath()

    for files_path in listdir(directory):
        # check if current path is a file
        if (path.splitext(files_path)[1] == '.json') and path.isfile(path.join(directory, files_path)):
            try:
                saves.append(_readFile(files_path))
            except:  # noqa: E722
                print(Fore.YELLOW + "There was an error with one save file" + Style.RESET_ALL)
    return (saves)


# read a save file and return data as object
def _readFile(filename: str) -> object:
    """
    Read file and parse it as json
    :filename: name of the file
    :return: data in json
    """
    filepath = path.join(_getSaveDirectoryPath(), filename)
    handler = open(filepath)
    state = load(handler)
    handler.close()
    return (state)


# Create a new file path
def _getFile(fileId: str = '') -> str:
    """
    Get file path
    :fileId:str the id of the file
    :return:str the path of the file
    """
    _ensureSaveDirectoryExists()
    directory = _getSaveDirectoryPath()
    filename = fileId + '.json'
    filepath = path.join(directory, filename)
    return (filepath)


# Get save directory path
def _getSaveDirectoryPath() -> str:
    """
    Get save directory path
    :return: str
    """
    global ROOT_DIR
    return path.join(ROOT_DIR, 'saves')


# Make sure save directory exists in filesystem
def _ensureSaveDirectoryExists() -> None:
    """
    Check if the directory exist else create it
    :return:None
    """
    global ROOT_DIR
    if not (path.exists(_getSaveDirectoryPath())):
        mkdir(_getSaveDirectoryPath())


# Save current simulation state
def saveState() -> None:
    """
    Set pause and send data to save
    :return: None
    """
    global pause, main_grid, ant_grid, width, height

    update_widgets()
    # First stop simulation
    pause = -1
    # Prepare data
    save({
        "width": width,
        "height": height,
        "generation": generation,
        "main_grid": main_grid,
        "ant_grid": ant_grid
    })


def loadState() -> None:
    """
    Set pause and dispaly list of save
    :return: None
    """
    global pause
    # Stop simmulation
    pause = -1
    saves = listSaves()
    window = Tk()
    window.title('Select a save file:')

    # Set the geometry
    window.geometry("600x600")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)

    if len(saves) == 0:
        emptyLabel = Label(window, text="No saves for now", anchor='center')
        emptyLabel.pack(pady=10)
    else:
        for iteration in range(0, len(saves)):
            save = saves[iteration]
            saveLabel = Label(window, text=save['saveName'], anchor="w", cursor="hand2")
            saveLabel.pack()
            saveLabel.bind("<Button-1>", lambda event, save=save: loadEntry(save, window))
            saveDate = datetime.fromtimestamp(save['createdAt'])
            saveUpdate = datetime.fromtimestamp(save['updatedAt'])
            saveInfo = "Created at : " + saveDate.strftime("%d/%m/%Y, %H:%M:%S") + " - Last update : " + saveUpdate.strftime("%d/%m/%Y, %H:%M:%S")
            dateLabel = Label(window, text=saveInfo, anchor="w", font=("Times New Roman", 8))
            dateLabel.pack()


def loadEntry(save: dict, window: Tk) -> None:
    """
    Set date from json file
    :save: dict an object containing the dates, id , name and state of the save entry
    :window: a window tkinter
    :return: None
    """
    global main_grid, ant_grid, width, height, generation
    main_grid = save['state']['main_grid']
    ant_grid = save['state']['ant_grid']
    width = save['state']['width']
    height = save['state']['height']
    generation = save['state']['generation']
    window.destroy()
    update_widgets()

# /=> Save functions END <=/
# /=> Dependancies END <=/


def Rectangle(grid, x, y, x_length, y_length, value=1):
    """
    Used to create a rectangle based on coordinates.
    Used by the place_action function, that triggers when there's a click.
    """

    limit = (width - 2) * (height - 2)
    if x_length * y_length >= limit:
        Sim_feedback.config(text="Cannot place a full grid.", fg="#FF0000")
        return (0)
    elif (x + x_length + 1 > len(grid[0])) and (y + y_length + 1 > len(grid)) or (x <= 0 and y <= 0):
        Sim_feedback.config(text="Cannot place out of bounds in x and y axis.", fg="#FF0000")
        return (0)
    elif (x + x_length + 1 > len(grid[0])) or (x <= 0):
        Sim_feedback.config(text="Cannot place out of bounds in x axis.", fg="#FF0000")
        return (0)
    elif (y + y_length + 1 > len(grid)) or (y <= 0):
        Sim_feedback.config(text="Cannot place out of bounds in y axis.", fg="#FF0000")
        return (0)
    else:
        Sim_feedback.config(text="Nothing to report.", fg="#00AA00")

        for xp in range(x_length):
            for yp in range(y_length):
                grid[y + yp][x + xp] = value


# /=> Simulation parameters <=/

height, width, posx, posy, pause = 100, 100, 10, 10, -1
# Dimensions correction (Border)
height += 2
width += 2

main_grid, ant_grid = start(height, width), start_ant(height, width)

action, cursor_size_width, cursor_size_height = (Rectangle), 1, 1

generation, number_of_generations, steps_per_gen = 0, .99999e5, 1
slide, cell = 1, 9

# [cell color, ant color 1, ant color 2] [name]
rules = [["#000000", "#ff00ff", "#ffff00"], "LANGTON ANT"]

dimensions = ((width * (cell)), (height * (cell)))

base_font = ("Times New Roman", 12)

# /=> Simulation parameters END <=/


def stop_sim():
    '''Set the simulation parameters so that it stops itself.'''

    global generation, number_of_generations, pause
    print(Fore.RED + 'Attempted a forced window closure at generation n° %d at %s  ' % (generation, time_log()) + Style.RESET_ALL)
    generation = number_of_generations
    pause = 1


def clear_grid():
    '''Clear both grids and reset to it's base state.'''

    global main_grid, ant_grid, generation
    main_grid = start(height, width)
    ant_grid = start_ant(height, width)
    generation = 0
    draw_simulation()
    update_widgets()


def fill_grid(grid=main_grid, value=-1, tmp=1):
    '''Fill both grids.'''

    for row in range(1, height - 1):  # Ignore the edges
        for column in range(1, width - 1):    # Ignore the edges
            if tmp:
                grid[row][column] = value
            else:
                grid[row][column] = -(grid[row][column])

# /=> Window DEF <=/


main_window = Tk()
main_window.title("Langton's Ant")
main_window.configure(bg="#2C3E50")
main_window.state(windowState)
main_window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))

try:
    windows_icons = PhotoImage(file="langton_icon.png")
    main_window.iconphoto(False, windows_icons)
except:  # noqa: E722
    print(Fore.RED + "Could not load the window icon." + Style.RESET_ALL)

# /=> Window DEF END <=/

# /=> Widgets DEF <=/
sim_graph = Label()
sim_graph.grid(row=0, column=2, rowspan=height * 20, columnspan=3, padx=10)

setting = LabelFrame(main_window, text="Settings", padx=50, pady=10, bg="#17202A", fg="#FFFFFF")
setting.grid(row=0, column=0)
com = LabelFrame(main_window, text="Command", padx=185, pady=10, bg="#17202A", fg="#FFFFFF")
com.grid(row=1, column=0)

Sim_time = Label(setting, text="N/A", background="#111111", fg='#ff8000', font=base_font)
Sim_date = Label(setting, text="N/A", background="#111111", fg='#ff8000', font=base_font)
Sim_Dimensions = Label(setting, text="N/A", background="#111111", fg='#0088ff', font=base_font)
Sim_current_coordinates_x = Label(setting, text="N/A", background="#111111", fg='#0088ff', font=base_font)
Sim_current_coordinates_y = Label(setting, text="N/A", background="#111111", fg='#0088ff', font=base_font)
Sim_stats_dimensions = Label(setting, text="N/A", background="#111111", fg='#0088ff', font=base_font)
Sim_feedback = Label(setting, text="Nothing to report.", background="#111111", fg="#AAAAAA", font=base_font)
Sim_generation = Label(setting, text="N/A", background="#111111", fg='magenta', font=base_font)
Sim_cells = Label(setting, text="N/A", background="#111111", fg='magenta', font=base_font)
Sim_ant = Label(setting, text="N/A", background="#111111", fg='magenta', font=base_font)
Sim_progress = Label(setting, text="N/A", background="#111111", font=base_font)


grid_edit = IntVar()
grid_Checkbutton = Checkbutton(com, bg="#FFCCBC", text="Edit Cells", variable=grid_edit, width=15, selectcolor='#FBAFFF', indicatoron=0)

Simulation_fill_white = Button(com, text='Fill White', command=lambda: fill_grid(main_grid, value=-1), bg="#87CEEB", width=15)
Simulation_fill_black = Button(com, text='Fill Black', command=lambda: fill_grid(main_grid, value=1), bg="#FFD54F", width=15)
Simulation_reverse = Button(com, text='Invert White/Black', command=lambda: fill_grid(main_grid, tmp=0), bg="#EC7063", width=15)
Simulation_clear = Button(com, text='Clear', command=lambda: clear_grid(), bg="#58D68D", width=15)
Simulation_save = Button(com, text="Save", command=lambda: saveState(), bg="#5DADE2", width=15)
Simulation_load = Button(com, text="Load", command=lambda: loadState(), bg="#CBAACB", width=15)


Sim_time.grid(row=0, column=0, columnspan=2)
Sim_date.grid(row=1, column=0, columnspan=2, pady=5)
Sim_Dimensions.grid(row=2, column=0, columnspan=2)
Sim_current_coordinates_x.grid(row=3, column=0, pady=5)
Sim_current_coordinates_y.grid(row=3, column=1, pady=5)
Sim_stats_dimensions.grid(row=4, column=0, columnspan=2)
Sim_feedback.grid(row=5, column=0, columnspan=2, pady=5)
Sim_generation.grid(row=6, column=0, columnspan=2, pady=5)
Sim_cells.grid(row=7, column=0, columnspan=2)
Sim_ant.grid(row=8, column=0, columnspan=2, pady=5)
Sim_progress.grid(row=9, column=0, columnspan=2, pady=5)

grid_Checkbutton.grid(row=0, column=0)
Simulation_clear.grid(row=1, column=0, pady=5)
Simulation_fill_white.grid(row=2, column=0)
Simulation_fill_black.grid(row=3, column=0, pady=5)
Simulation_reverse.grid(row=4, column=0)
Simulation_save.grid(row=5, column=0, pady=5)
Simulation_load.grid(row=6, column=0)

Butexit = Button(com, text="Exit", width=15, command=lambda: stop_sim(), bg="#E1A5AC")
Butexit.grid(row=7, column=0, pady=5)


# /=> Widgets DEF END <=/


def update_widgets():
    '''Will update most widgets. Called with every cicle.'''
    Sim_time.config(text='Time: %s' % (time_log(True, True)))
    Sim_date.config(text='Date: %s' % (time_log(True, False, False)))
    Sim_generation.config(text="Generation: %.5d | Max: %.5d" % (generation, number_of_generations))
    Sim_cells.config(text='Cell(s): %s' % count(main_grid, 0))
    Sim_ant.config(text='Ant(s): %s' % count(ant_grid))
    Sim_progress.config(text=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[0], fg=progress_bar(generation, number_of_generations, tmp=1, tmp2=4)[1])
    Sim_stats_dimensions.config(text='Cursor dimensions: %dx%d | %s' % (cursor_size_width, cursor_size_height, str(action.__name__)))


def draw_simulation():
    '''Function used for the graphic aspect of the code.'''

    images_standart_size = (width, height)
    cell_grid = Image.new("RGBA", images_standart_size, "#FFFFFF")
    pixels = cell_grid.load()
    x_sim, y_sim = ((sim_graph.winfo_pointerx() - sim_graph.winfo_rootx()) // cell) * cell, ((sim_graph.winfo_pointery() - sim_graph.winfo_rooty()) // cell) * cell

    for row in range(width):
        for column in range(height):
            # Draw black pixels if there's a cell.
            if main_grid[column][row] == 1:
                pixels[row, column] = conv_hex_rgb(rules[0][0])

            # Draw border's pixels if iterating at the borders.
            if (column in [0, len(main_grid) - 1] or row in [0, len(main_grid[0]) - 1]):
                pixels[row, column] = conv_hex_rgb('#000088')

            # Draw ant's pixels if there's an ant, based on if there's a cell underneath.
            if ant_grid[column][row][0] == 1:
                pixels[row, column] = conv_hex_rgb(rules[0][1]) if (main_grid[column][row] == 1) else conv_hex_rgb(rules[0][2])

    # Resize the image to be bigger.
    mid_image = ((cell_grid.resize((cell_grid.size[0] * cell, cell_grid.size[1] * cell), resample=Image.NEAREST)))

    # Draw pixels intersections as points, red if the cell is marked, black otherwise.
    pixels = mid_image.load()
    for row in range(width):
        for column in range(height):
            if not ((column in [0, len(main_grid) - 1] or row in [0, len(main_grid[0]) - 1])):
                pixels[row * cell, column * cell] = (255, 0, 0) if (main_grid[column][row] == 1 or main_grid[column - 1][row - 1] == 1 or main_grid[column][row - 1] == 1 or main_grid[column - 1][row] == 1) else (0, 0, 0)

    if (cell <= x_sim <= dimensions[0] - cursor_size_width - 1 * cell and cell <= y_sim <= dimensions[1] - cursor_size_height - 1 * cell) and (dimensions[0] - (x_sim + (cursor_size_width) * cell) > 0) and (dimensions[1] - (y_sim + (cursor_size_height) * cell) > 0):
        for length_cursor in range(cursor_size_width * cell):
            pixels[x_sim + length_cursor, y_sim - 1] = (255, 0, 0)
            pixels[x_sim + length_cursor, y_sim + cursor_size_height * cell - 1] = (255, 0, 0)
        for height_cursor in range(cursor_size_height * cell):
            pixels[x_sim, y_sim + height_cursor - 1] = (255, 0, 0)
            pixels[x_sim + cursor_size_width * cell, y_sim + height_cursor - 1] = (255, 0, 0)

    final_image = ImageTk.PhotoImage(mid_image)
    sim_graph.configure(image=final_image)
    sim_graph.image = final_image


def main_cycle():
    '''Rules to select the next behaviour of the simulation.'''

    global main_grid, ant_grid, generation, number_of_generations

    if pause == 1:
        update_widgets()

    curs_x, curs_y = ((sim_graph.winfo_pointerx() - sim_graph.winfo_rootx()) // cell), ((sim_graph.winfo_pointery() - sim_graph.winfo_rooty()) // cell)
    if (0 <= curs_x < width):
        Sim_current_coordinates_x.config(text='Cursor pos x: %d' % (curs_x))
    if ((0 <= curs_y < height)):
        Sim_current_coordinates_y.config(text='Cursor pos y: %d' % (curs_y))
    main_window.update()
    draw_simulation()
    if pause == -1:
        draw_simulation()
        main_window.after(func=main_cycle, ms=1)
    elif generation < number_of_generations:
        for iteration in range(steps_per_gen):
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height, slide, steps_per_gen)
        generation += steps_per_gen
        main_window.after(func=main_cycle, ms=1)
    else:
        main_window.destroy()


def place_action(eventorigin):
    '''Action of creating a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [1, "N"]), (main_grid, 1)][int(grid_edit.get())]
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])


def destroy_cell(eventorigin):
    '''Action of destroying a cell.'''

    reg_x, reg_y = (eventorigin.x) // cell, (eventorigin.y) // cell
    grid_and_action = [(ant_grid, [0, "N"]), (main_grid, -1)][int(grid_edit.get())]
    action(grid_and_action[0], reg_x, reg_y, cursor_size_width, cursor_size_height, grid_and_action[1])


def key_press(event):
    '''Assign actions to keyboard key.'''
    global pause, main_grid, ant_grid, generation, cursor_size_height, cursor_size_width

    Sim_Dimensions.config(text='Dimensions: %dx%d px' % dimensions)
    press = event.keysym
    if press == 'space':
        update_widgets()
        pause = -(pause)
    elif press == 'f':
        pause = -1
        if generation >= number_of_generations:
            main_window.destroy()
        else:
            main_grid, ant_grid = next_gen(main_grid, ant_grid, width, height, slide, steps_per_gen)
            generation += 1
            update_widgets()
    elif press == 'd':
        pause = -1
        if generation >= number_of_generations:
            main_window.destroy()
        else:
            main_grid, ant_grid = previous_gen(main_grid, ant_grid, width, height, slide, steps_per_gen)
            generation += 1
            update_widgets()
    elif press == 'Tab':
        stop_sim()
    elif press == 'Up':
        if cursor_size_height < height - 2:
            cursor_size_height += 1
    elif press == 'Down':
        if 1 < cursor_size_height:
            cursor_size_height -= 1
    elif press == 'Right':
        if cursor_size_width < width - 2:
            cursor_size_width += 1
    elif press == 'Left':
        if 1 < cursor_size_width:
            cursor_size_width -= 1


# /=> START <=/

main_window.bind('<Key>', key_press)
sim_graph.bind("<B1-Motion>", place_action)
sim_graph.bind("<Button-1>", place_action)
sim_graph.bind("<B3-Motion>", destroy_cell)
sim_graph.bind("<Button-3>", destroy_cell)

main_window.after(func=main_cycle, ms=0)
update_widgets()

main_window.mainloop()
