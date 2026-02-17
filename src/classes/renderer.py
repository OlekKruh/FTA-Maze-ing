from .grid import Grid
from .cell import Cell
from .menu import Menu
from .graphics import Graphics
import random
import time
import sys


class Renderer:
    def __init__(self, grafix_module: Graphics, menu_module: Menu) -> None:
        self.gfx = grafix_module
        self.menu = menu_module

    @staticmethod
    def clear_screen() -> None:
        """
        \033[2J - очистить все
        \033[H  - курсор домой (левый верхний угол)
        """
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    @staticmethod
    def hide_cursor() -> None:
        """
        \033[?25l - скрыть курсор (чтобы не мигал)
        """
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_cursor() -> None:
        """
        \033[?25h - показать курсор (нужно перед input)
        """
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def save_cursor() -> None:
        sys.stdout.write("\0337")
        sys.stdout.flush()

    @staticmethod
    def restore_cursor() -> None:
        sys.stdout.write("\0338")
        sys.stdout.flush()

    @staticmethod
    def move_cursor(x: int, y: int) -> None:
        """
        Внутренний метод прыжка.
        ВАЖНО: ANSI координаты начинаются с 1, а не с 0.
        Порядок: Строка (Y), Колонка (X).
        """
        sys.stdout.write(f"\033[{y};{x}H")

    @staticmethod
    def type_text(text: str,
                  min_delay: float = 0.04,
                  max_delay: float = 0.09) -> None:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(random.uniform(min_delay, max_delay))

    @staticmethod
    def backspace(count: int,
                  min_delay: float = 0.04,
                  max_delay: float = 0.09) -> None:
        for _ in range(count):
            sys.stdout.write("\b \b")
            sys.stdout.flush()
            time.sleep(random.uniform(min_delay, max_delay))

    def draw_cell(self, cell: Cell,
                  delay: float = 0.02) -> None:
        screen_y = cell.cell_y + 1
        screen_x = cell.cell_x + 1

        char = self.gfx.get_char_for_cell(cell)
        color = self.gfx.get_color_for_cell(cell)
        reset = self.gfx.current_theme_map["RESET"]

        self.move_cursor(screen_x, screen_y)
        sys.stdout.write(f"{color}{char}{reset}")
        sys.stdout.flush()
        time.sleep(delay)

    def redraw_grid(self, grid: Grid) -> None:
        self.hide_cursor()
        for row in grid.matrix:
            for cell in row:
                self.draw_cell(cell, 0)
        self.show_cursor()

    def update_menu_line(self, maze_height: int, line_index: int) -> None:
        current_y = maze_height + 2 + line_index

        menu_list = self.menu.get_current_list(
            path_visible=self.gfx.show_path,
            char_style=self.gfx.current_style_name,
            color_style=self.gfx.current_theme_name
        )
        text = menu_list[line_index]
        self.move_cursor(1, current_y)
        sys.stdout.write("\033[K")
        self.type_text(text, 0, 0)
        sys.stdout.flush()

    def render_all(self, grid: Grid):
        self.clear_screen()

        menu_list = self.menu.get_current_list(
            path_visible=self.gfx.show_path,
            char_style=self.gfx.current_style_name,
            color_style=self.gfx.current_theme_name
        )

        for row in grid.matrix:
            for cell in row:
                self.draw_cell(cell)

        self.move_cursor(1, grid.grid_height + 1)
        print(" " * grid.grid_width)

        for i in range(len(menu_list)):
            self.update_menu_line(grid.grid_height, i)

        self.show_cursor()
