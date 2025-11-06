import arcade
from game.characters.player import Player
from game.characters.stats import Stats
from game.items.inventory import Inventory

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Noxy"

ATTACK_FLASH_TIME = 0.15
STOP_DISTANCE = 5.0  # pixels


class GameView(arcade.View):
    """Main game screen: holds the Player, handles input/update/draw."""

    def __init__(self) -> None:
        super().__init__()
        # Create a simple player using your classes
        stats = Stats(move_speed=220.0, max_hp=10, attack_speed=1.5)
        inv = Inventory(size=40)
        self.player = Player(
            name="Noxy",
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5),
            stats=stats,
            inventory=inv,
            current_hp=stats.max_hp,
            exp=0,
            money=0,
            level=1,
        )

        # Movement state
        self._moving_with_rmb: bool = False
        self._move_target: tuple[float, float] | None = None

        # Attack feedback
        self._attack_time_left: float = 0.0

        # HUD
        self._title = arcade.Text(
            "RMB: hold to move  |  LMB: attack",
            16, SCREEN_HEIGHT - 32, arcade.color.WHITE, 16
        )

    def on_show_view(self) -> None:
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self) -> None:
        """Render the frame."""
        self.clear()

        # Move target marker
        if self._move_target is not None:
            tx, ty = self._move_target
            arcade.draw_circle_outline(tx, ty, 10, arcade.color.LIGHT_GRAY, 2)
            arcade.draw_line(tx - 14, ty, tx + 14, ty, arcade.color.LIGHT_GRAY, 2)
            arcade.draw_line(tx, ty - 14, tx, ty + 14, arcade.color.LIGHT_GRAY, 2)

        # Player (simple circle + shadow)
        px, py = self.player.pos
        arcade.draw_ellipse_filled(px, py - 10, 28, 10, (0, 0, 0, 110))
        arcade.draw_circle_filled(px, py, 14, arcade.color.ALMOND)
        arcade.draw_circle_outline(px, py, 14, arcade.color.BLACK, 1)

        # Attack flash
        if self._attack_time_left > 0:
            t = 1.0 - (self._attack_time_left / ATTACK_FLASH_TIME)
            radius = 18 + 20 * t
            arcade.draw_circle_outline(px, py, radius, arcade.color.GOLD, 3)

        # HUD
        self._title.draw()

    def on_update(self, dt: float) -> None:
        """Game logic per frame."""
        # Move while RMB is held
        if self._moving_with_rmb and self._move_target is not None:
            px, py = self.player.pos
            tx, ty = self._move_target
            dx, dy = (tx - px), (ty - py)
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= STOP_DISTANCE:
                self._move_target = None
            else:
                nx, ny = (dx / dist), (dy / dist)
                speed = self.player.stats.move_speed
                step = speed * dt
                if step > dist:
                    step = dist
                self.player.pos = (px + nx * step, py + ny * step)

        # Attack flash timer
        if self._attack_time_left > 0:
            self._attack_time_left -= dt
            if self._attack_time_left < 0:
                self._attack_time_left = 0

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Mouse press: RMB = start moving, LMB = attack flash."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self._moving_with_rmb = True
            self._move_target = (x, y)
        elif button == arcade.MOUSE_BUTTON_LEFT:
            self._attack_time_left = ATTACK_FLASH_TIME

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Stop moving when RMB is released."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self._moving_with_rmb = False
            self._move_target = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """While RMB is held, keep updating the target to the cursor."""
        if self._moving_with_rmb:
            self._move_target = (x, y)
