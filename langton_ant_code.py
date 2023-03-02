from colorama import init, Fore, Style
from datetime import datetime

init()

angles = ["E", "N", "O", "S"]


def time_log(simple_format=0):  # Will estimate the precise time at which it has been executed  # noqa: E501
    if simple_format == 1:
        return ('%s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    return ('[%s]: ' % (datetime.now().strftime("%d/%m/%Y | %H:%M:%S")))


def progress_bar(progress, total, init_msg='', end_msg='', mode=0):
    percent, current_time = (progress * 100) / float(total), time_log(1)
    if percent % 2 == 0:
        bar = '▓' * int((percent)/2) + '░' * (int((100 - percent)/2))
    else:
        bar = '▓' * int((percent)/2) + '░' * (int((100 - percent)/2) + 1)

    if mode == 0:
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


def count(table, mode=1):
    count = 0
    for y in range(len(table)):
        for x in range(len(table[0])):
            if mode:
                count += (table[y][x][0] if table[y][x][0] > 0 else 0)
            else:
                count += (table[y][x] if table[y][x] > 0 else 0)
    percentage = ((count * 100) / ((len(table) - 2) * (len(table[0]) - 2)))
    return str(count) + ' / ' + str((len(table) - 2) * (len(table[0]) - 2)) + ' ' + '({:.02f}%)'.format(percentage)  # noqa: E501


def start(height, width, value=-1):
    return ([[-1 for _ in range(width)] for _ in range(height)])


def start_ant(height, width, value=[0, "N"]):
    return ([[[0, "N"] for _ in range(width)] for _ in range(height)])


def render(table):
    for index in range(len(table)):
        print(*table[index], end='\n')


def read(table, x, y):
    return (table[y][x])


def read_ant(table, x, y, mode=1):
    if mode:
        return (table[y][x][0])
    return (table[y][x][1])


def case_selector(direction, value, multiplier=1):

    if value:
        return multiplier * [[0, 1], [-1, 0], [0, -1], [1, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501
    return multiplier * [[0, -1], [1, 0], [0, 1], [-1, 0]][["E", "N", "O", "S"].index(direction)]  # noqa: E501


def interval(x, length_grid):
    if 1 <= x < length_grid-1:
        return x
    elif x == 0:
        return length_grid-2
    else:
        return (x % (length_grid-1)) + 1


def next_gen(previous_table_main, previous_table_ant, width, height):
    new_table_main = start(len(previous_table_main), len(previous_table_main[0]))  # noqa: E501
    new_table_ant = start_ant(len(previous_table_ant), len(previous_table_ant[0]))  # noqa: E501

    for x in range(1, len(previous_table_ant[0]) - 1):
        for y in range(1, len(previous_table_ant) - 1):
            # [Cell State], [Turn, Cell change, Movement], [Cell color], [Rule Name]  # noqa: E501

            # Keep cells in their state
            if previous_table_main[y][x] == 1:
                new_table_main[y][x] = 1

            if previous_table_ant[y][x][0]:     # If there is an ant
                if previous_table_main[y][x] == -1:     # If the cell is white
                    directions = case_selector(previous_table_ant[y][x][1], -1, 2)    # Select ant's new orientation  # noqa: E501
                    new_table_ant[interval(y+directions[0], height)][interval(x+directions[1], width)] = [1, angles[(angles.index(previous_table_ant[y][x][1])-1) % 4]]    # Generate new ant's attributes  # noqa: E501
                else:
                    directions = case_selector(previous_table_ant[y][x][1], 1, 2)  # noqa: E501
                    new_table_ant[interval(y-directions[0], height)][interval(x-directions[1], width)] = [1,  angles[(angles.index(previous_table_ant[y][x][1])+1) % 4]]  # noqa: E501
                new_table_main[y][x] = -previous_table_main[y][x]   # Switch cell state  # noqa: E501

    return (new_table_main, new_table_ant)


if __name__ == '__main__':
    pass
