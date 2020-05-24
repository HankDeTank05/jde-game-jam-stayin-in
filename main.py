import random

import arcade
import worldgrid

TILE_SIZE = 32

WALL_WIDTH = 32
WALL_DEPTH = 8

SCREEN_BORDER = 20

SCREEN_SCALE = 1

WIDTH = TILE_SIZE
HEIGHT = TILE_SIZE
MARGIN = WALL_DEPTH
COLUMN_COUNT = 17
ROW_COUNT = 17

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "JDE Project"

MOVE_SPEED = 1
PLAYER_SIZE = 12


class Player(arcade.Sprite):

    def update(self, left_coll: bool, right_coll: bool, top_coll: bool, bottom_coll: bool):
        if left_coll and self.change_x < 0:
            pass
        if right_coll and self.change_x > 0:
            pass
        if top_coll and self.change_y > 0:
            pass
        if bottom_coll and self.change_y < 0:
            pass
        self.center_x += self.change_x
        self.center_y += self.change_y

        # add collision detection here
        pass


# NOTE: for the wall sprites, if the row number of the array is odd, they will be rotated vertically. Otherwise,
# they wont be rotated

class Wall(arcade.Sprite):

    def __init__(self, solid: bool, center_x: int, center_y: int, scale: float, vertical: bool = False):
        if solid:
            super().__init__('sprites/wall_00.png', scale=scale)
        else:
            super().__init__('sprites/log_00.png', scale=scale)

        if vertical:
            self.angle = random.choice([90, 270])
        else:
            self.angle = 0

        self.center_x = center_x
        self.center_y = center_y

    def update(self):
        if self.angle >= 360:
            self.angle -= 360


class Game(arcade.Window):
    """
    Main application class
    """

    def __init__(self, width, height, title):
        """
        constructor
        :param width:
        :param height:
        :param title:
        """
        super().__init__(width, height, title)

        self.player1 = None

        self.player2 = None

        self.grid = None

        self.sprite_array = []

        self.player_list = None
        self.wooden_wall_list = None
        self.solid_wall_list = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self, size_x: int = COLUMN_COUNT, size_y: int = ROW_COUNT, center_size: int = 2):
        """
        setup the game
        :param size: the size of the grid (at least 27)
        :param center_size: the size of the center meetup area (at least 2)
        :return:
        """

        self.player1 = Player('sprites/p1_32_0.png', scale=SCREEN_SCALE)
        self.player2 = Player('sprites/p2_32_0.png', scale=SCREEN_SCALE)

        self.grid = worldgrid.generate(COLUMN_COUNT, ROW_COUNT, center_size)
        # self.grid[self.p1_y][self.p1_x] = '1'
        # self.grid[self.p2_y][self.p2_x] = '2'

        self.solid_wall_list = arcade.SpriteList()
        self.wooden_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        for y in range(len(self.grid)):
            self.sprite_array.append([])
            for x in range(len(self.grid[y])):
                sprite_x = x * WALL_WIDTH + WALL_WIDTH // 2 + ((x - 1) * WALL_DEPTH)
                sprite_y = y * WALL_WIDTH + WALL_WIDTH // 2 + ((y - 1) * WALL_DEPTH)
                vertical = None
                # if y is odd and x is even, vertical = True
                if y % 2 == 1 and x % 2 == 0:
                    vertical = True
                # if y is odd and x is odd, do nothing
                # if y is even and x is even, it's a dot-wall, not a thin wall
                # if y is even and x is odd, vertical = False
                elif y % 2 == 0 and x % 2 == 1:
                    vertical = False
                if self.grid[y][x] == 'S':
                    self.solid_wall_list.append(Wall(True, sprite_x, sprite_y, SCREEN_SCALE, vertical))
                elif self.grid[y][x] == 'W':
                    self.wooden_wall_list.append(Wall(False, sprite_x, sprite_y, SCREEN_SCALE, vertical))
                elif self.grid[y][x] == '1':
                    self.player1.center_x = sprite_x
                    self.player1.center_y = sprite_y
                    self.player1.angle += 180
                    print(sprite_x, sprite_y)
                elif self.grid[y][x] == '2':
                    self.player2.center_x = sprite_x
                    self.player2.center_y = sprite_y
                    print(sprite_x, sprite_y)
                else:
                    self.sprite_array[y].append(None)

        self.player_list.append(self.player1)
        self.player_list.append(self.player2)

    def on_update(self, delta_time: float):
        """
        process the game logic
        :param delta_time:
        :return:
        """
        # self.player1.center_x = self.p1_x * TILE_SIZE + TILE_SIZE // 2
        # self.player1.center_y = self.p1_y * TILE_SIZE + TILE_SIZE // 2

        left_coll = False
        right_coll = False
        top_coll = False
        bottom_coll = False
        wooden_wall_hit_list1 = arcade.check_for_collision_with_list(self.player1, self.wooden_wall_list)
        for wall in wooden_wall_hit_list1:
            if wall.top <= self.player1.top < wall.bottom:
                print('wood top coll')
                top_coll = True
            if wall.bottom <= self.player1.bottom < wall.top:
                print('wood bottom coll')
                bottom_coll = True
            if wall.left <= self.player1.left < wall.right:
                print('wood left coll')
                left_coll = True
            if wall.right >= self.player1.right > wall.left:
                print('wood right coll')
                right_coll = True
        solid_wall_hit_list1 = arcade.check_for_collision_with_list(self.player1, self.solid_wall_list)
        self.player1.update(left_coll, right_coll, top_coll, bottom_coll)

        # self.player2.center_x = self.p2_x * TILE_SIZE + TILE_SIZE // 2
        # self.player2.center_y = self.p2_y * TILE_SIZE + TILE_SIZE // 2

        # self.player2.update()
    def on_draw(self):
        """
        update the screen
        :return:
        """
        arcade.start_render()

        self.solid_wall_list.draw()
        self.wooden_wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """
        process player input
        :param symbol:
        :param modifiers:
        :return:
        """
        # process input for player 1
        if symbol == arcade.key.W:
            self.player1.change_y = MOVE_SPEED  # move up
            # print('w')
        if symbol == arcade.key.A:
            self.player1.change_x = -MOVE_SPEED  # move left
            # print('a')
        if symbol == arcade.key.S:
            self.player1.change_y = -MOVE_SPEED  # move down
            # print('s')
        if symbol == arcade.key.D:
            self.player1.change_x = MOVE_SPEED  # move right
            # print('d')

        # process input for player 2
        if symbol == arcade.key.UP:
            pass  # move up
        if symbol == arcade.key.LEFT:
            pass  # move left
        if symbol == arcade.key.DOWN:
            pass  # move down
        if symbol == arcade.key.RIGHT:
            pass  # move right

        if symbol == arcade.key.RSHIFT:
            pass  # spin player 1's buzzsaw

        if symbol == arcade.key.LSHIFT:
            pass  # spin player 2's buzzsaw

    def on_key_release(self, symbol: int, modifiers: int):

        # reset the movement deltas for player 1
        if symbol in [arcade.key.W, arcade.key.S]:
            # print('release y')
            self.player1.change_y = 0
        if symbol in [arcade.key.A, arcade.key.D]:
            # print('release x')
            self.player1.change_x = 0


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
