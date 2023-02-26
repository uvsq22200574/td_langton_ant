def render(table):
    for index in range(len(table)):
        print(*table[index], end='\n')


def start(height, width):
    return ([[-1 for _ in range(width)] for _ in range(height)])


def start_ant(height, width):
    return ([[[0, "N"] for _ in range(width)] for _ in range(height)])


def topile(pile, pil):
    return (pile + [pil])


def unpile(pile):
    return (pile[:-1], pile[-1])


if __name__ == '__main__':
    pass
