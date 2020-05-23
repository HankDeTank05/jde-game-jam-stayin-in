import random


def generate(size: int = 27, center_size: int = 2):
    grid = []

    # make sure the size is at least 27 and is an odd number
    if size <= 27:
        size = 27
    elif size % 2 == 0:
        size += 1

    # make sure the center_size is at least 2 and an even number
    if center_size < 2:
        center_size = 2
    elif center_size % 2 == 1:
        center_size += 1

    # create an easy reference variable for the range representing the area of the center
    mid_range = range(size//2-center_size, size//2+center_size+1)

    for y in range(size):
        grid.append([])
        for x in range(size):
            if x == 0 or y == 0 or x == size - 1 or y == size - 1:
                grid[y].append('X')
            elif x in mid_range and y in mid_range:
                grid[y].append(' ')
            elif x % 2 == 0 and y % 2 == 0:
                grid[y].append('S')
            elif x % 2 == 0 or y % 2 == 0:
                grid[y].append(random.choice(['W', 'W', 'S']))
            else:
                grid[y].append(' ')

            print(grid[y][x], end=' ')
        print()

    return grid
