import arcade
from scenes.game_view import GameView

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Noxy"

def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    window.show_view(GameView())
    arcade.run()

if __name__ == "__main__":
    main()
