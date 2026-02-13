from typing import Optional

from . import MazeConfig, Grid, Graphics, Menu, Renderer
import sys
import time


class Manager:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.grid = Grid(config.maze_width, config.maze_height)
        self.gfx = Graphics()
        self.menu = Menu()
        self.renderer = Renderer(self.gfx, self.menu)
        self.is_path_visible = False

    def run(self):
        self.renderer.render_all(self.grid, self.is_path_visible)
        while True:
            try:
                command = self.menu.get_user_choice()
            except ValueError:
                continue

            match command:
                case self.menu.CMD_EXIT:
                    self.renderer.clear_screen()
                    print("[SYSTEM]: Hasta la vista, baby.")
                    sys.exit()

                case self.menu.CMD_GENERATE_NEW:
                    self._stub_action("Запуск алгоритма генерации...",
                                      command)

                case self.menu.CMD_SHOW_PATH:
                    self.is_path_visible = not self.is_path_visible
                    self._stub_action(f"Режим показа пути: "
                                      f"{self.is_path_visible}",
                                      command)
                    # включить подсветку пути обновить строку в меню

                case self.menu.CMD_CHAR_STYLE:
                    self.gfx.toggle_style()
                    self._stub_action(f"Стиль изменен на: "
                                      f"{self.gfx.current_style_name}",
                                      command)
                    # перерисовка лаберинта и изменение строки в меню

                case self.menu.CMD_CHANGE_COLORS:
                    self.gfx.toggle_theme()
                    self._stub_action(f"Тема изменена на: "
                                      f"{self.gfx.current_theme_name}",
                                      command)
                    # перерисовка лаберинта и изменение строки в меню

                case _:
                    self._stub_action("Неизвестная команда", command)

    def _stub_action(self, message: str, command: Optional[int, str]):
        # if isinstance(command, int):
        #     command = 1
        # else:
        #     command = len(command)
        command = 1 if isinstance(command, int) else len(command)

        msg_y = self.grid.grid_height + 9
        full_massage = f">>> STUB: {message}"

        self.renderer.move_cursor(1, msg_y)
        sys.stdout.write(f"\033[K")
        # sys.stdout.write(f">> STUB: {message}")
        self.renderer.type_text(full_massage)
        sys.stdout.flush()

        time.sleep(3)  # Даем прочитать

        # Стираем сообщение
        self.renderer.backspace(len(full_massage))
        # стираем комманду
        outset = len(self.menu.get_choice()) + 1 + command
        self.renderer.move_cursor(outset, msg_y - 1)
        self.renderer.backspace(command)
        sys.stdout.flush()
