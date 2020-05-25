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
COLUMN_COUNT = 21
ROW_COUNT = 21

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "JDE Project"

MOVE_SPEED = 1
PLAYER_SIZE = 12

P1_CONTROLS = {
    'left': arcade.key.A,
    'right': arcade.key.D,
    'up': arcade.key.W,
    'down': arcade.key.S,
    'buzzsaw': arcade.key.F
}

P2_CONTROLS = {
    'left': arcade.key.K,
    'right': arcade.key.SEMICOLON,
    'up': arcade.key.O,
    'down': arcade.key.L,
    'buzzsaw': arcade.key.J
}


class Player(arcade.Sprite):
    def __init__(self, filename: str, controls: dict, scale: float, starting_ammo: int = 2):
        super().__init__(filename, scale)
        # print(f"__init__ controls['left'] = {controls['left']}")
        # print(f"__init__ controls['right'] = {controls['right']}")
        self.move_left = int(controls['left'])
        self.move_right = int(controls['right'])
        self.move_up = controls['up']
        self.move_down = controls['down']
        self.activate_other_buzzsaw = controls['buzzsaw']

        self.sawblades_remaining = starting_ammo

        # print(f"Player.left = {self.left}")
        # print(f"Player.right = {self.right}")

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def handle_collision(self, direction: str):
        if direction in ['l', 'r', 't', 'b']:  # left, right, top bottom
            if (direction == 'l' and self.change_x < 0) or (direction == 'r' and self.change_x > 0):
                self.change_x = 0

            if (direction == 't' and self.change_y > 0) or (direction == 'b' and self.change_y < 0):
                self.change_y = 0

    def handle_collision_with_list(self, wall_list: list):
        for wall in wall_list:
            if self.top >= wall.bottom > self.center_y:
                # print('wood top coll')
                self.handle_collision('t')
            elif self.bottom <= wall.top < self.center_y:
                # print('wood bottom coll')
                self.handle_collision('b')
            elif self.left <= wall.right < self.center_x:
                # print('wood left coll')
                self.handle_collision('l')
            elif self.right >= wall.left > self.center_x:
                # print('wood right coll')
                self.handle_collision('r')

    def activate_buzzsaw(self, direction_vector: tuple):
        if self.sawblades_remaining > 0:
            # self.sawblades_remaining -= 1
            return MetalBlade(int(self.center_x), int(self.center_y), direction_vector)
        return


# NOTE: for the wall sprites, if the row number of the array is odd, they will be rotated vertically. Otherwise,
# they wont be rotated

class Wall(arcade.Sprite):

    def __init__(self, solid: bool, center_x: int, center_y: int, scale: float, vertical: bool = False):
        if solid:
            super().__init__('sprites/wall_00.png', scale=scale)
            self.textures = arcade.load_spritesheet('sprites/wall_spritesheet.png', 64, 16, 2, 15)
        else:
            super().__init__('sprites/log_00.png', scale=scale)
            self.textures = arcade.load_spritesheet('sprites/log_spritesheet.png', 64, 16, 2, 16)

        if vertical:
            self.angle = random.choice([90, 270])
        else:
            self.angle = 0

        self.center_x = center_x
        self.center_y = center_y
        self.breakable = not solid
        self.animate = False
        self.current_texture = 0
        self.animation_speed = 0.25

    def update(self):
        if self.animate:
            self.current_texture += self.animation_speed
            if self.current_texture % 1 == 0:
                self.current_texture = int(self.current_texture)
                if self.breakable and self.current_texture == len(self.textures):
                    self.remove_from_sprite_lists()
                elif not self.breakable and self.current_texture == len(self.textures):
                    self.animate = False
                    self.current_texture = 0
                    self.set_texture(self.current_texture)
                else:
                    self.set_texture(self.current_texture)

    def cut_wall(self):
        self.animate = True
        self.current_texture += 1


class MetalBlade(arcade.Sprite):

    def __init__(self, start_pos_x: int, start_pos_y: int, direction: tuple):
        super().__init__('sprites/sawblade_0.png')
        self.center_x = start_pos_x
        self.center_y = start_pos_y

        self.current_texture = 0
        self.textures = arcade.load_spritesheet('sprites/sawblade_spritesheet.png', 16, 16, 3, 8)

        self.change_x = direction[0]
        self.change_y = direction[1]

        self.animation_speed = 0.25

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.current_texture += self.animation_speed
        if self.current_texture % 1 == 0:
            self.current_texture = int(self.current_texture)
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0


class Game(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        """
        constructor
        :param width:
        :param height:
        :param title:
        """
        super().__init__()

        self.player1 = None

        self.player2 = None

        self.maze = None
        self.grid = None

        self.sprite_array = []

        self.player_list = None
        self.wooden_wall_list = None
        self.solid_wall_list = None
        self.sawblade_list = None

        arcade.set_background_color(arcade.color.GO_GREEN)

    def setup(self, size_x: int = COLUMN_COUNT, size_y: int = ROW_COUNT, center_size: int = 2):
        """
        setup the game
        :param size_x:
        :param size_y:
        :param center_size: the size of the center meetup area (at least 2)
        :return:
        """

        self.player1 = Player('sprites/p1_32_0.png', controls=P1_CONTROLS, scale=SCREEN_SCALE)
        self.player2 = Player('sprites/p2_32_0.png', controls=P2_CONTROLS, scale=SCREEN_SCALE)

        self.maze = worldgrid.generate_maze((size_x-1)//2, (size_y-1)//2)
        self.grid = self.maze.maze

        self.solid_wall_list = arcade.SpriteList()
        self.wooden_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.sawblade_list = arcade.SpriteList()

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
                    self.solid_wall_list.append(
                        Wall(True, sprite_x, sprite_y, SCREEN_SCALE, vertical))  # append a solid wall to the list
                elif self.grid[y][x] == 'C':
                    sprite = arcade.SpriteSolidColor(WALL_DEPTH*2, WALL_DEPTH*2, arcade.color.DIM_GRAY)
                    sprite.center_x = sprite_x
                    sprite.center_y = sprite_y
                    self.solid_wall_list.append(sprite)
                    # print(f'c @ {x}, {y}')
                elif self.grid[y][x] == 'X' and (
                        ((y == 0 or y == size_y - 1) and x % 2 == 1) or ((x == 0 or x == size_x - 1) and y % 2 == 1)):
                    self.solid_wall_list.append(
                        Wall(True, sprite_x, sprite_y, SCREEN_SCALE, vertical))  # create the borders of the grid
                elif self.grid[y][x] == 'W':
                    self.wooden_wall_list.append(
                        Wall(False, sprite_x, sprite_y, SCREEN_SCALE, vertical))  # append a log to the list
                elif self.grid[y][x] == '1':
                    self.player1.center_x = sprite_x
                    self.player1.center_y = sprite_y
                    self.player1.angle += 180
                    # print(sprite_x, sprite_y)
                elif self.grid[y][x] == '2':
                    self.player2.center_x = sprite_x
                    self.player2.center_y = sprite_y
                    # print(sprite_x, sprite_y)
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

        wooden_wall_hit_list_1 = arcade.check_for_collision_with_list(self.player1, self.wooden_wall_list)
        solid_wall_hit_list_1 = arcade.check_for_collision_with_list(self.player1, self.solid_wall_list)
        self.player1.handle_collision_with_list(wooden_wall_hit_list_1)
        self.player1.handle_collision_with_list(solid_wall_hit_list_1)

        wooden_wall_hit_list_2 = arcade.check_for_collision_with_list(self.player2, self.wooden_wall_list)
        solid_wall_hit_list_2 = arcade.check_for_collision_with_list(self.player2, self.solid_wall_list)
        self.player2.handle_collision_with_list(wooden_wall_hit_list_2)
        self.player2.handle_collision_with_list(solid_wall_hit_list_2)

        if len(self.sawblade_list) > 0:
            for sawblade in self.sawblade_list:
                wooden_wall_collision_list = arcade.check_for_collision_with_list(sawblade, self.wooden_wall_list)
                solid_wall_collision_list = arcade.check_for_collision_with_list(sawblade, self.solid_wall_list)
                for wooden_wall in wooden_wall_collision_list:
                    wooden_wall.animate = True

                if len(wooden_wall_collision_list) > 0 or len(solid_wall_collision_list) > 0:
                    sawblade.remove_from_sprite_lists()

        self.wooden_wall_list.update()
        self.player_list.update()
        self.sawblade_list.update()

    def on_draw(self):
        """
        update the screen
        :return:
        """
        arcade.start_render()

        # arcade.draw_text("Controls: WASD = move blue. F = use red's sawblade. OKL; = move red. J = use blue's sawblade",
        #                  0, SCREEN_HEIGHT-30, arcade.color.BLACK)

        arcade.draw_text("WASD = move blue    F = use red's sawblade", 10, SCREEN_HEIGHT-18, arcade.color.BLUE)
        arcade.draw_text("OKL; = move red    J = use blue's sawblade", 10, SCREEN_HEIGHT-32, arcade.color.RED)
        arcade.draw_text("OBJECTIVE: meet in the center!", SCREEN_WIDTH//2, SCREEN_HEIGHT-28, arcade.color.BLACK)

        self.solid_wall_list.draw()
        self.wooden_wall_list.draw()
        self.player_list.draw()
        if len(self.sawblade_list) > 0:
            self.sawblade_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """
        process player input
        :param symbol:
        :param modifiers:
        :return:
        """
        # process input for player 1
        if symbol == self.player1.move_up:
            self.player1.change_y = MOVE_SPEED  # move up
            self.player1.angle = 180
            # print('w')
        if symbol == self.player1.move_left:
            self.player1.change_x = -MOVE_SPEED  # move left
            self.player1.angle = 270
            # print('a')
        if symbol == self.player1.move_down:
            self.player1.change_y = -MOVE_SPEED  # move down
            self.player1.angle = 0
            # print('s')
        if symbol == self.player1.move_right:
            self.player1.change_x = MOVE_SPEED  # move right
            self.player1.angle = 90
            # print('d')

        if symbol == self.player1.activate_other_buzzsaw:
            if self.player2.angle == 0:
                direction_vector = (0, -1)
            elif self.player2.angle == 90:
                direction_vector = (1, 0)
            elif self.player2.angle == 180:
                direction_vector = (0, 1)
            elif self.player2.angle == 270:
                direction_vector = (-1, 0)
            else:
                direction_vector = (0, 0)
            sawblade = self.player2.activate_buzzsaw(direction_vector)  # spin player 2's buzzsaw
            if sawblade is not None:
                self.sawblade_list.append(sawblade)

        # process input for player 2
        if symbol == self.player2.move_up:
            self.player2.change_y = MOVE_SPEED  # move up
            self.player2.angle = 180
        if symbol == self.player2.move_left:
            self.player2.change_x = -MOVE_SPEED  # move left
            self.player2.angle = 270
        if symbol == self.player2.move_down:
            self.player2.change_y = -MOVE_SPEED  # move down
            self.player2.angle = 0
        if symbol == self.player2.move_right:
            self.player2.change_x = MOVE_SPEED  # move right
            self.player2.angle = 90

        if symbol == self.player2.activate_other_buzzsaw:
            if self.player1.angle == 0:
                direction_vector = (0, -1)
            elif self.player1.angle == 90:
                direction_vector = (1, 0)
            elif self.player1.angle == 180:
                direction_vector = (0, 1)
            elif self.player1.angle == 270:
                direction_vector = (-1, 0)
            else:
                direction_vector = (0, 0)
            sawblade = self.player1.activate_buzzsaw(direction_vector)  # spin player 1's buzzsaw
            # print(type(sawblade))
            if sawblade is not None:
                self.sawblade_list.append(sawblade)

    def on_key_release(self, symbol: int, modifiers: int):

        # reset the movement deltas for player 1
        if symbol in [self.player1.move_up, self.player1.move_down]:
            # print('release y')
            self.player1.change_y = 0
        if symbol in [self.player1.move_left, self.player1.move_right]:
            # print('release x')
            self.player1.change_x = 0

        if symbol in [self.player2.move_up, self.player2.move_down]:
            self.player2.change_y = 0
        if symbol in [self.player2.move_left, self.player2.move_right]:
            self.player2.change_x = 0

        if symbol == self.player1.activate_other_buzzsaw:
            pass
        if symbol == self.player2.activate_other_buzzsaw:
            pass


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()

        self.p1_ready = False
        self.p1_controls = {
            arcade.key.W: False,
            arcade.key.A: False,
            arcade.key.S: False,
            arcade.key.D: False,
            arcade.key.F: False
        }

        self.p2_ready = False
        self.p2_controls = {
            arcade.key.O: False,
            arcade.key.K: False,
            arcade.key.L: False,
            arcade.key.SEMICOLON: False,
            arcade.key.J: False
        }

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.FOREST_GREEN)

        # reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_update(self, delta_time):
        if not self.p1_ready:
            self.p1_ready = True
            for key in self.p1_controls.keys():
                if not self.p1_controls[key]:
                    self.p1_ready = False
                    break

        if not self.p2_ready:
            self.p2_ready = True
            for key in self.p2_controls.keys():
                if not self.p2_controls[key]:
                    self.p2_ready = False
                    break

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("How To Play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WOOD_BROWN, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.p1_controls.keys():
            self.p1_controls[symbol] = True

        if symbol in self.p2_controls.keys():
            self.p2_controls[symbol] = True

    def on_mouse_press(self, x, y, button, modifiers):
        """ If the user presses the mouse button, start the game """
        if self.p1_ready and self.p2_ready:
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    # start_view.setup()

    arcade.run()


if __name__ == "__main__":
    main()
