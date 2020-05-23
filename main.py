import arcade
import worldgrid

GRID_SIZE = 27

TILE_SIZE = 32
TILE_SPACE = 2

WALL_WIDTH = 32
WALL_DEPTH = 8

SCREEN_BORDER = 20

SCREEN_SCALE = 1

SCREEN_WIDTH = SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE
SCREEN_TITLE = "JDE Project"

MOVE_SPEED = 1
PLAYER_SIZE = 12


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # add collision detection here
        pass


class SolidWall(arcade.SpriteSolidColor):

    def __init__(self, center_x, center_y):
        super().__init__(TILE_SIZE, TILE_SIZE, arcade.color.DARK_GRAY)
        self.center_x = center_x
        self.center_y = center_y


class WoodenWall(arcade.SpriteSolidColor):

    def __init__(self, center_x, center_y):
        super().__init__(TILE_SIZE, TILE_SIZE, arcade.color.WOOD_BROWN)
        self.center_x = center_x
        self.center_y = center_y


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
        self.p1_pos = []
        self.p1_x = None
        self.p1_y = None
        self.p1_move = []

        self.player2 = None
        self.p2_pos = []
        self.p2_x = None
        self.p2_y = None
        self.p2_move = []

        self.grid = None

        self.sprite_array = []

        self.sprite_list = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self, size: int = 27, center_size: int = 2):
        """
        setup the game
        :param size: the size of the grid (at least 27)
        :param center_size: the size of the center meetup area (at least 2)
        :return:
        """
        self.p1_x = 1
        self.p1_y = 1
        self.player1 = Player('sprites/p1_32_0.png', scale=SCREEN_SCALE)

        self.p2_x = size - 2
        self.p2_y = size - 2
        self.player2 = Player('sprites/p2_32_0.png', scale=SCREEN_SCALE)

        self.grid = worldgrid.generate(size, center_size)
        self.grid[self.p1_y][self.p1_x] = '1'
        self.grid[self.p2_y][self.p2_x] = '2'
        self.sprite_list = arcade.SpriteList()

        for y in range(len(self.grid)):
            self.sprite_array.append([])
            for x in range(len(self.grid[y])):
                if self.grid[y][x] in ['S', 'X']:
                    self.sprite_array[y].append(SolidWall(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                    self.sprite_list.append(self.sprite_array[y][x])
                elif self.grid[y][x] == 'W':
                    self.sprite_array[y].append(WoodenWall(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                    self.sprite_list.append(self.sprite_array[y][x])
                elif self.grid[y][x] == '1':
                    self.sprite_array[y].append(self.player1)
                    self.sprite_list.append(self.player1)
                elif self.grid[y][x] == '2':
                    self.sprite_array[y].append(self.player2)
                    self.sprite_list.append(self.player2)
                else:
                    self.sprite_array[y].append(None)

        self.sprite_list.append(self.player1)
        self.sprite_list.append(self.player2)

    def on_update(self, delta_time: float):
        """
        process the game logic
        :param delta_time:
        :return:
        """
        self.player1.center_x = self.p1_x * TILE_SIZE + TILE_SIZE // 2
        self.player1.center_y = self.p1_y * TILE_SIZE + TILE_SIZE // 2

        self.player1.update()

        self.player2.center_x = self.p2_x * TILE_SIZE + TILE_SIZE // 2
        self.player2.center_y = self.p2_y * TILE_SIZE + TILE_SIZE // 2

        self.player2.update()

    def on_draw(self):
        """
        update the screen
        :return:
        """
        arcade.start_render()

        # draw the objects in the shape list
        self.sprite_list.draw()

        # draw the sprites in the sprite list
        self.sprite_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """
        process player input
        :param symbol:
        :param modifiers:
        :return:
        """
        # process input for player 1
        if symbol == arcade.key.W:
            pass  # move up
            print('w')
        if symbol == arcade.key.A:
            pass  # move left
            print('a')
        if symbol == arcade.key.S:
            pass  # move down
            print('s')
        if symbol == arcade.key.D:
            pass  # move right
            print('d')

        # process input for player 2
        if symbol in [arcade.key.UP, arcade.key.LEFT, arcade.key.DOWN, arcade.key.RIGHT]:
            self.grid[self.p2_y][self.p2_x] = ' '
            if symbol == arcade.key.UP:
                pass  # move up
            if symbol == arcade.key.LEFT:
                pass  # move left
            if symbol == arcade.key.DOWN:
                pass  # move down
            if symbol == arcade.key.RIGHT:
                pass  # move right
            self.grid[self.p2_y][self.p2_x] = '2'

        if symbol == arcade.key.RSHIFT:
            pass  # spin player 1's buzzsaw

        if symbol == arcade.key.LSHIFT:  # spin player 2's buzzsaw
            if symbol == arcade.key.UP and self.grid[self.p2_y-1][self.p2_x] == 'W':
                pass
            if symbol == arcade.key.LEFT and self.grid[self.p2_y][self.p2_x-1] == 'W':
                pass
            if symbol == arcade.key.DOWN and self.grid[self.p2_y+1][self.p2_x] == 'W':
                pass
            if symbol == arcade.key.RIGHT and self.grod[self.p2_y][self.p2_x+1] == 'W':
                pass


    def on_key_release(self, symbol: int, modifiers: int):
        pass


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
