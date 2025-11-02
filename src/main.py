import arcade
import json
import os
import math
from typing import Optional, Tuple

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Noxy"

PLAYER_SPEED = 240.0
STOP_DISTANCE = 6.0
ATTACK_FLASH_TIME = 0.12

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "saves")
SAVE_PATH = os.path.join(SAVE_DIR, "state.json")


class GameView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((40, 80, 85))

        self.player_pos: Tuple[float, float] = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5)
        self.move_target: Optional[Tuple[float, float]] = None

        self.attack_time_left = 0.0

        self.title_text = arcade.Text("Noxy — Prototype 0.1", 16, SCREEN_HEIGHT - 32, arcade.color.WHITE, 16)
        self.hint_text = arcade.Text(
            "RMB: move  |  LMB: attack  |  A/S/D/F/G: abilities  |  F5: save  |  F9: load",
            16, SCREEN_HEIGHT - 56, arcade.color.LIGHT_GRAY, 14,
        )
        self.status_text = arcade.Text("", 16, 16, arcade.color.WHITE, 14)
        self._status_timer = 0.0

        self._ensure_save_dir()
        if os.path.exists(SAVE_PATH):
            self._load_state()
            self._set_status("Loaded state.", 1.5)
        else:
            self._set_status("New session.", 1.0)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.move_target = (x, y)
            self._set_status(f"Moving to ({int(x)}, {int(y)})", 0.9)
        elif button == arcade.MOUSE_BUTTON_LEFT:
            self.attack_time_left = ATTACK_FLASH_TIME
            self._set_status("Attack!", 0.5)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F5:
            self._save_state()
            self._set_status("Saved.", 1.0)
            return
        if symbol == arcade.key.F9:
            self._load_state()
            self._set_status("Loaded.", 1.0)
            return
        if symbol in (arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.F, arcade.key.G):
            key_to_ability = {arcade.key.A: "A", arcade.key.S: "S", arcade.key.D: "D",
                              arcade.key.F: "F", arcade.key.G: "G"}
            self._set_status(f"Ability {key_to_ability[symbol]}", 0.6)

    def on_update(self, delta_time: float):
        if self.move_target is not None:
            px, py = self.player_pos
            tx, ty = self.move_target
            dx, dy = (tx - px), (ty - py)
            dist = math.hypot(dx, dy)

            if dist <= STOP_DISTANCE:
                self.move_target = None
            else:
                nx, ny = (dx / dist), (dy / dist)
                px += nx * PLAYER_SPEED * delta_time
                py += ny * PLAYER_SPEED * delta_time
                self.player_pos = (px, py)

        if self.attack_time_left > 0:
            self.attack_time_left -= delta_time
            if self.attack_time_left < 0:
                self.attack_time_left = 0

        if self._status_timer > 0:
            self._status_timer -= delta_time
            if self._status_timer <= 0:
                self.status_text.text = ""

    def on_draw(self):
        self.clear()

        if self.move_target is not None:
            tx, ty = self.move_target
            arcade.draw_circle_outline(tx, ty, 10, arcade.color.LIGHT_GRAY, 2)
            arcade.draw_line(tx - 14, ty, tx + 14, ty, arcade.color.LIGHT_GRAY, 2)
            arcade.draw_line(tx, ty - 14, tx, ty + 14, arcade.color.LIGHT_GRAY, 2)

        px, py = self.player_pos
        arcade.draw_ellipse_filled(px, py - 10, 28, 10, (0, 0, 0, 110))
        arcade.draw_circle_filled(px, py, 14, arcade.color.ALMOND)
        arcade.draw_circle_outline(px, py, 14, arcade.color.BLACK, 1)

        if self.attack_time_left > 0:
            t = 1.0 - (self.attack_time_left / ATTACK_FLASH_TIME)
            radius = 18 + 20 * t
            arcade.draw_circle_outline(px, py, radius, arcade.color.GOLD, 3)

        self.title_text.draw()
        self.hint_text.draw()
        self.status_text.draw()

    def _ensure_save_dir(self):
        os.makedirs(SAVE_DIR, exist_ok=True)

    def _save_state(self):
        self._ensure_save_dir()
        px, py = self.player_pos
        data = {"player": {"x": float(px), "y": float(py)}}
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            px = float(data.get("player", {}).get("x", self.player_pos[0]))
            py = float(data.get("player", {}).get("y", self.player_pos[1]))
            self.player_pos = (px, py)
        except Exception:
            pass

    def _set_status(self, text: str, seconds: float):
        self.status_text.text = text
        self._status_timer = seconds


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()
