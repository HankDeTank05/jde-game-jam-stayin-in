import random

world = []

world_size = 10
mid_size = 2

if world_size <= 27:
    world_size = 27
if world_size % 2 == 0:
    world_size += 1

mid_range = range(world_size//2-mid_size, world_size//2+mid_size+1)

for y in range(world_size):
    world.append([])
    for x in range(world_size):
        if x == 0 or y == 0 or x == world_size - 1 or y == world_size - 1:
            world[y].append('X')
        elif x in mid_range and y in mid_range:
            world[y].append(' ')
        elif x % 2 == 0 and y % 2 == 0:
            world[y].append('S')
        elif x % 2 == 0 or y % 2 == 0:
            world[y].append(random.choice(['W', 'W', 'S']))
        else:
            world[y].append(' ')

        print(world[y][x], end=' ')
    print()
