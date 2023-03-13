from colorama import init, Fore, Style

init()


def time_log(simple_format=False):  # noqa: E501
    from datetime import datetime
    '''Will estimate the precise time at which it has been executed.'''
    if simple_format is True:
        return ('%s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    return ('[%s]: ' % (datetime.now().strftime("%d/%m/%Y | %H:%M:%S")))


def progress_bar(progress: int, total: int, init_msg='', end_msg='', tmp=0, tmp2=2):  # noqa: E501
    '''Returns or print a progress bar.'''
    percent, current_time = (progress * 100) / float(total), time_log(True)
    if percent % 2 == 0:
        bar = '▓' * int((percent)/tmp2) + '░' * (int((100 - percent)/tmp2))
    else:
        bar = '▓' * int((percent)/tmp2) + '░' * (int((100 - percent)/tmp2) + 1)

    if tmp == 0:
        if progress/total >= 1:
            print(Fore.GREEN + '╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + end_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
        elif progress/total >= .5:
            print(Fore.YELLOW + '╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
        else:
            print(Fore.RED + '╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + init_msg + Style.RESET_ALL, sep=' ', end='\r')  # noqa: E501
    else:
        if progress/total >= 1:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + end_msg + '\r', "#00FF00")  # noqa: E501
        elif progress/total >= .5:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + init_msg + '\r', "#FFFF00")  # noqa: E501
        else:
            return ('╠%s╣ %.3f %% at %s' % (bar, percent, current_time) + ' ' + init_msg + '\r', "#FF0000")  # noqa: E501


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
    return str(count) + ' / ' + str((len(table) - 2) * (len(table[0]) - 2)) + ' ' + '({:.02f}%)'.format(percentage)  # noqa: E501


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

    if cell_state:
        return multiplier * [[0, 1], [-1, 0], [0, -1], [1, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501
    return multiplier * [[0, -1], [1, 0], [0, 1], [-1, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501


def interval(x: int, length_grid: int):
    '''
    Enable the grid to be a tor.
    '''
    if 1 <= x < length_grid-1:
        return x
    elif x == 0:
        return length_grid-2
    return (x % (length_grid-1)) + 1


def next_gen(previous_table_main: list, previous_table_ant: list, width: int, height: int):  # noqa:501
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
                    directions = case_selector(previous_table_ant[y][x][1], -1, 2)    # Select ant's new orientation  # noqa: E501
                    new_table_ant[interval(y+directions[0], height)][interval(x+directions[1], width)] = [1, angles[(angles.index(previous_table_ant[y][x][1])-1) % 4]]  # Set new ant's attributes  # noqa: E501
                else:
                    directions = case_selector(previous_table_ant[y][x][1], 1, 2)  # noqa: E501
                    new_table_ant[interval(y-directions[0], height)][interval(x-directions[1], width)] = [1,  angles[(angles.index(previous_table_ant[y][x][1])+1) % 4]]  # noqa: E501
                new_table_main[y][x] = -previous_table_main[y][x]   # Switch cell state  # noqa: E501

    return (new_table_main, new_table_ant)


if __name__ == '__main__':
    pass
