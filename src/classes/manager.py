from typing import Optional
from . import MazeConfig, Grid, Graphics, Menu, Renderer
import sys
import time


class Manager:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.grid = Grid(config)
        self.gfx = Graphics()
        self.menu = Menu()
        self.renderer = Renderer(self.gfx, self.menu)
        self.is_path_visible = False

    def run(self):
        self.renderer.render_all(self.grid)
        while True:
            try:
                command = self.menu.get_user_choice()
            except ValueError:
                continue

            match command:
                case self.menu.CMD_EXIT:
                    self._handle_exit()

                case self.menu.CMD_GENERATE_NEW:
                    self.update_menu_line(command)

                case self.menu.CMD_SHOW_PATH:
                    self.update_menu_line(command)

                case self.menu.CMD_CHAR_STYLE:
                    self.gfx.toggle_style()
                    self.update_menu_line(command)

                case self.menu.CMD_CHANGE_COLORS:
                    self.gfx.toggle_theme()
                    self.update_menu_line(command)

                case _:
                    self.update_menu_line(command)

    def _handle_exit(self):
        self.renderer.clear_screen()
        print("[SYSTEM]: Hasta la vista, baby.")
        sys.exit(0)

    def _handle_generate(self, command):
        self._stub_action("Запуск алгоритма генерации...", command)
        # self.builder.run() ...

    def _handle_unknown(self, command):
        self._stub_action("Unknown command", command)

    def update_menu_line(self, command: int):
        prompt_len = len(self.menu.get_choice()) + command
        sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
        self.renderer.backspace(command)

        self.renderer.save_cursor()
        self.renderer.update_menu_line(self.grid.grid_height, command)
        self.renderer.redraw_grid(self.grid)
        self.renderer.restore_cursor()

    def _stub_action(self, message: str, command: Optional[int, str]):
        command = 1 if isinstance(command, int) else len(command)

        msg_y = self.grid.grid_height + 9
        full_massage = f">>> STUB: {message}"

        self.renderer.move_cursor(1, msg_y)
        sys.stdout.write("\033[K")
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
