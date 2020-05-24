import random

MIN_GRID_SIZE = 11

def generate(size_x: int = 17, size_y: int = 17, center_size: int = 2):
    grid = []

    # make sure the size is at least 27 and is an odd number
    if size_x <= MIN_GRID_SIZE:
        size_x = MIN_GRID_SIZE
    elif size_x % 2 == 0:
        size_x += 1

    if size_y <= MIN_GRID_SIZE:
        size_y = MIN_GRID_SIZE
    elif size_y % 2 == 0:
        size_y += 1

    # make sure the center_size is at least 2 and an even number
    if center_size < 2:
        center_size = 2
    elif center_size % 2 == 1:
        center_size += 1

    # create an easy reference variable for the range representing the area of the center
    mid_range_x = range(size_x//2-center_size, size_x//2+center_size+1)
    mid_range_y = range(size_y//2-center_size, size_y//2+center_size+1)

    for y in range(size_y):
        grid.append([])
        for x in range(size_x):
            if x == 0 or y == 0 or x == size_x - 1 or y == size_y - 1 or (x % 2 == 0 and y % 2 == 0):
                grid[y].append('X')
            elif x in mid_range_x and y in mid_range_y:
                if (x == mid_range_x.start or x == mid_range_x.stop-1) or (y == mid_range_y.start or y == mid_range_y.stop-1):
                    grid[y].append('W')
                else:
                    grid[y].append(' ')
            elif x % 2 == 0 or y % 2 == 0:
                grid[y].append(random.choice(['W', 'S']))
            elif x == 1 and y == 1:
                grid[y].append('1')
            elif x == size_x-2 and y == size_y-2:
                grid[y].append('2')
            else:
                grid[y].append(' ')

            print(grid[y][x], end=' ')
        print()

    return grid

# generate()