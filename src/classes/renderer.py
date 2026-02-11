from . import Grid, Cell, Menu, Graphics
import sys


class Renderer:
    def __init__(self, grafix_module: Graphics, menu_module: Menu) -> None:
        self.gfx = grafix_module
        self.menu = menu_module

    def clear_screen(self) -> None:
        """
        \033[2J - очистить все
        \033[H  - курсор домой (левый верхний угол)
        """
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def hide_cursor(self) -> None:
        """
        \033[?25l - скрыть курсор (чтобы не мигал)
        """
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self) -> None:
        """
        \033[?25h - показать курсор (нужно перед input)
        """
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def seve_cursore(self) -> None:
        sys.stdout.write("\033[s")
        sys.stdout.flush()

    def restore_cursore(self) -> None:
        sys.stdout.write("\033[u")
        sys.stdout.flush()

    def _move_cursor(self, x: int, y: int) -> None:
        """
        Внутренний метод прыжка.
        ВАЖНО: ANSI координаты начинаются с 1, а не с 0.
        Порядок: Строка (Y), Колонка (X).
        """
        sys.stdout.write(f"\033[{y};{x}H")

    def draw_cell(self, cell: Cell) -> None:
        screen_y = cell.y + 1
        screen_x = cell.x + 1

        char = self.gfx.get_char_for_cell(cell)
        color = self.gfx.get_color_for_cell(cell)
        reset = self.gfx.current_theme_map["RESET"]

        self.seve_cursore()
        self._move_cursor(screen_x, screen_y)
        sys.stdout.write(f"{color}{char}{reset}")
        self.restore_cursore()
        sys.stdout.flush()

    def update_menu_line(self, text: str, maze_height: int, line_index: int) -> None:
        current_y = maze_height + 2 + line_index

        self.seve_cursore()
        self._move_cursor(1, current_y)
        sys.stdout.write(f"\033[K{text}")
        self.restore_cursore()
        sys.stdout.flush()

    def render_all(self, grid: Grid, menu_lines: list):
        self.clear_screen()
        self.restore_cursore()

        for row in grid.matrix:
            for cell in row:
                self.draw_cell(cell)

        self._move_cursor(1, grid.grid_height + 1)
        print("=" * grid.grid_width)

        for i, line in enumerate(menu_lines):
            self.update_menu_line(line, grid.grid_height, i)

        self.show_cursor()


