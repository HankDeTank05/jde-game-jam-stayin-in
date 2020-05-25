import random
import worldmap

MIN_GRID_SIZE = 11


def generate(size_x: int = 17, size_y: int = 17, center_size: int = 2):
    grid = worldmap.Maze(size_x, size_y)

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
    mid_range_x = range(size_x // 2 - center_size, size_x // 2 + center_size + 1)
    mid_range_y = range(size_y // 2 - center_size, size_y // 2 + center_size + 1)

    for y in range(size_y):
        grid.append([])
        for x in range(size_x):
            if x == 0 or y == 0 or x == size_x - 1 or y == size_y - 1 or (x % 2 == 0 and y % 2 == 0):
                grid[y].append('X')
            elif x in mid_range_x and y in mid_range_y:
                if (x == mid_range_x.start or x == mid_range_x.stop - 1) or (
                        y == mid_range_y.start or y == mid_range_y.stop - 1):
                    grid[y].append('W')
                else:
                    grid[y].append(' ')
            elif x % 2 == 0 or y % 2 == 0:
                grid[y].append(random.choice(['W', 'W', 'W', 'W', 'S', 'S', 'S']))
            elif x == 1 and y == 1:
                grid[y].append('1')
            elif x == size_x - 2 and y == size_y - 2:
                grid[y].append('2')
            else:
                grid[y].append(' ')

            print(grid[y][x], end=' ')
        print()

    return grid


def generate_maze(cell_x, cell_y):
    return_maze = worldmap.Maze(cell_x, cell_y)
    size_x = cell_x*2+1
    size_y = cell_y*2+1
    return_maze.generate_with_recursive_backtracking(cell_x // 2, cell_y // 2)
    mid_range_x = range(size_x // 2 - 2, size_x // 2 + 2 + 1)
    mid_range_y = range(size_y // 2 - 2, size_y // 2 + 2 + 1)
    for y in range(len(return_maze.maze)):
        for x in range(len(return_maze.maze[y])):
            if x % 2 == 0 and y % 2 == 0:
                return_maze.maze[y][x] = 'C'
            elif x in mid_range_x and y in mid_range_y and (x == mid_range_x.start or x == mid_range_x.stop-1 or y == mid_range_y.start or y ==mid_range_y.stop-1):
                return_maze.maze[y][x] = 'W'
            elif x in mid_range_x and y in mid_range_y:
                return_maze.maze[y][x] = ' '

    return_maze.maze[1][1] = '1'
    return_maze.maze[size_y-2][size_x-2] = '2'
    return return_maze


if __name__ == "__main__":
    # generate()

    # maze_x = 10
    # maze_y = 10
    # maze = worldmap.Maze(maze_x, maze_y)
    # maze.generate_with_recursive_backtracking(maze_x // 2, maze_y // 2)
    maze = generate_maze(10, 10)
    print(maze)
