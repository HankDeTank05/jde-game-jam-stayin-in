import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "JDE Project"


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

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
