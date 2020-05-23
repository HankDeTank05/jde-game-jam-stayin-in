import arcade
import worldgrid

GRID_SIZE = 27

TILE_SIZE = 16

WALL_THICKNESS = 10
SCREEN_BORDER = 20

SCREEN_SCALE = 2

SCREEN_WIDTH = SCREEN_HEIGHT = (GRID_SIZE * TILE_SIZE) - WALL_THICKNESS + (2 * SCREEN_BORDER)
SCREEN_TITLE = "JDE Project"

MAP_SIZE = 27

MOVE_SPEED = TILE_SIZE + WALL_THICKNESS
PLAYER_SIZE = int(TILE_SIZE * 0.9)


class Player(arcade.SpriteSolidColor):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < SCREEN_BORDER + WALL_THICKNESS:
            self.left = SCREEN_BORDER + WALL_THICKNESS
        if self.right > SCREEN_WIDTH - 1 - (SCREEN_BORDER + WALL_THICKNESS):
            self.right = SCREEN_WIDTH - 1 - (SCREEN_BORDER + WALL_THICKNESS)

        if self.top > SCREEN_HEIGHT - 1 - (SCREEN_BORDER + WALL_THICKNESS):
            self.top = SCREEN_HEIGHT - 1 - (SCREEN_BORDER + WALL_THICKNESS)
        if self.bottom < SCREEN_BORDER + WALL_THICKNESS:
            self.bottom = SCREEN_BORDER + WALL_THICKNESS


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
        self.p1_move = []

        self.player2 = None
        self.p2_pos = []
        self.p2_move = []

        self.grid = None

        self.shape_list = None
        self.sprite_list = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self, size: int = 27, center_size: int = 2):
        """
        setup the game
        :param size: the size of the grid (at least 27)
        :param center_size: the size of the center meetup area (at least 2)
        :return:
        """
        self.player1 = Player(PLAYER_SIZE, PLAYER_SIZE, arcade.color.BLUE)
        self.p1_pos = [TILE_SIZE//2 + SCREEN_BORDER + WALL_THICKNESS, TILE_SIZE//2 + SCREEN_BORDER + WALL_THICKNESS]
        self.p1_move = [0, 0]

        self.player2 = Player(PLAYER_SIZE, PLAYER_SIZE, arcade.color.RED)
        self.p2_pos = [TILE_SIZE//2 + SCREEN_BORDER + WALL_THICKNESS, TILE_SIZE//2 + SCREEN_BORDER + WALL_THICKNESS]
        self.p2_move = [0, 0]

        self.grid = worldgrid.generate(size, center_size)

        self.shape_list = arcade.ShapeElementList()
        self.sprite_list = arcade.SpriteList()

        self.sprite_list.append(self.player1)
        self.sprite_list.append(self.player2)

    def on_update(self, delta_time: float):
        """
        process the game logic
        :param delta_time:
        :return:
        """

        # move player 1
        self.p1_pos[0] += self.p1_move[0]
        self.p1_pos[1] += self.p1_move[1]
        self.player1.center_x = self.p1_pos[0]
        self.player1.center_y = self.p1_pos[1]

        self.player1.update()

        self.p1_move = [0, 0]

        # move player 2
        self.p2_pos[0] += self.p2_move[0]
        self.p2_pos[1] += self.p2_move[1]
        self.player2.center_x = self.p2_pos[0]
        self.player2.center_y = self.p2_pos[1]

        self.player2.update()

        self.p2_move = [0, 0]

    def on_draw(self):
        """
        update the screen
        :return:
        """
        arcade.start_render()

        # draw the objects in the shape list
        self.shape_list.draw()

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
            self.player1.change_y += MOVE_SPEED  # move up
        if symbol == arcade.key.A:
            self.player1.change_x -= MOVE_SPEED  # move left
        if symbol == arcade.key.S:
            self.player1.change_y -= MOVE_SPEED  # move down
        if symbol == arcade.key.D:
            self.player1.change_x += MOVE_SPEED  # move right

        # process input for player 2
        if symbol == arcade.key.UP:
            self.p2_move[1] += MOVE_SPEED  # move up
        if symbol == arcade.key.LEFT:
            self.p2_move[0] -= MOVE_SPEED  # move left
        if symbol == arcade.key.DOWN:
            self.p2_move[1] -= MOVE_SPEED  # move down
        if symbol == arcade.key.RIGHT:
            self.p2_move[0] += MOVE_SPEED  # move right

        if symbol == arcade.key.QUESTION:
            pass  # spin player 1's buzzsaw

        if symbol == arcade.key.E:
            pass  # spin player 2's buzzsaw

    def on_key_release(self, symbol: int, modifiers: int):
        # reset movement delta vector for player 1
        if symbol in [arcade.key.A, arcade.key.D]:
            self.p1_move[0] = 0
        if symbol in [arcade.key.W, arcade.key.S]:
            self.p1_move[1] = 0

        # reset movement delta vector for player 2
        if symbol in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.p2_move[0] = 0
        if symbol in [arcade.key.UP, arcade.key.DOWN]:
            self.p2_move[1] = 0
        pass


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
