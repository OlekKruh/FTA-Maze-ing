"""
The central controller for the A-Maze-Ing application.
"""

from __future__ import annotations

import sys
import time
from typing import Tuple, Union, Optional

from .builder import OriginShift, DFSBuilder, PrimBuilder
from .generators import GeneratorRegistry
from .grid import Grid
from .graphics import Graphics
from .maze_config import MazeConfig
from .menu import Menu
from .renderer import Renderer
from .solver import Solver

# Type aliases for clarity
Coord = Tuple[int, int]
Cmd = Union[int, str, None]


class Manager:
    """Application controller: coordinates generation, rendering, and IO."""

    def __init__(self, config: MazeConfig) -> None:
        self.config = config

        self.grid = Grid(config)
        self.gfx = Graphics()
        self.menu = Menu()
        self.renderer = Renderer(self.gfx, self.menu)

        self.registry = GeneratorRegistry(
            generators={
                "origin_shift": OriginShift(self.grid),
                "dfs_backtracker": DFSBuilder(self.grid),
                "prim": PrimBuilder(self.grid),
            },
            order=("origin_shift", "dfs_backtracker", "prim")
        )
        self.is_path_visible = False

    def run(self):
        self.renderer.render_all(self.grid,
                                 self.registry.current().name)
        while True:
            try:
                command = self.menu.get_user_choice()
            except ValueError:
                continue

            match command:
                case self.menu.CMD_EXIT:
                    self._handle_exit()

                case self.menu.CMD_GENERATE_NEW:
                    self._handle_generate(command)

                case self.menu.CMD_SHOW_PATH:
                    self._handle_show_path(command)

                case self.menu.CMD_CHAR_STYLE:
                    self.gfx.toggle_style()
                    self._update_menu_line_smart(command, redraw_grid=True)

                case self.menu.CMD_CHANGE_COLORS:
                    self.gfx.toggle_theme()
                    self._update_menu_line_smart(command, redraw_grid=True)

                case self.menu.CMD_CHANGE_GENERATOR:
                    self.registry.next()
                    self._update_menu_line_smart(command, redraw_grid=False)

                case _:
                    self._handle_unknown(command)

    def _handle_exit(self):
        self._stub_action("Hasta la vista, baby.", 5)
        self.renderer.clear_screen()
        sys.exit(0)

    def _handle_generate(self, command):
        prompt_len = len(self.menu.get_choice()) + len(str(command))
        sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
        self.renderer.backspace(len(str(command)))

        builder = self.registry.current()
        builder.setup()

        self.renderer.save_cursor()
        self.renderer.redraw_grid(self.grid)

        total_cells = self.grid.grid_width * self.grid.grid_height
        iterations = total_cells * 10

        for _ in range(iterations):
            changed_cells = builder.step()

            if not changed_cells:
                break

            for cell in changed_cells:
                self.renderer.draw_cell(cell, delay=0.005)

        self.renderer.restore_cursor()

    def _handle_unknown(self, command: Cmd):
        self._stub_action("Unknown command", command)

    def _update_menu_line_smart(self, command: int, redraw_grid: bool):
        cmd_str = str(command)
        prompt_len = len(self.menu.get_choice()) + len(cmd_str)

        sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
        self.renderer.backspace(len(cmd_str))

        self.renderer.save_cursor()

        self.renderer.update_menu_line(
            self.grid.grid_height,
            command, self.registry.current().name)

        if redraw_grid:
            self.renderer.redraw_grid(self.grid)

        self.renderer.restore_cursor()

    def _stub_action(self, message: str, command: Cmd):
        command_len = 1 if isinstance(command, int) else len(str(command))

        msg_y = self.grid.grid_height + len(self.menu.menu_list) + 2
        full_message = f">>> {message}"

        self.renderer.move_cursor(1, msg_y)
        sys.stdout.write("\033[K")
        self.renderer.type_text(full_message)
        sys.stdout.flush()

        time.sleep(3)

        self.renderer.backspace(len(full_message))
        outset = len(self.menu.get_choice()) + 1 + command_len
        self.renderer.move_cursor(outset, msg_y - 1)
        self.renderer.backspace(command_len)
        sys.stdout.flush()

    def _handle_show_path(self, command: int):
        """Toggles the solution path visibility and solves the maze if needed."""
        # 1. Переключаем флаг видимости
        self.gfx.show_path = not self.gfx.show_path

        # 2. Если включили показ — ищем путь
        if self.gfx.show_path:
            solver = Solver(self.grid)

            start_coord = None
            exit_coord = None

            for row in self.grid.matrix:
                for cell in row:
                    if cell.is_start:
                        start_coord = (cell.cell_x, cell.cell_y)
                    elif cell.is_exit:
                        exit_coord = (cell.cell_x, cell.cell_y)

            if start_coord and exit_coord:
                result = solver.solve(start_coord, exit_coord)

                # --- НОВАЯ ПРОВЕРКА ---
                if not result.path_coords:
                    self._stub_action("Path not found! Maze might be broken.", command)
                    self.gfx.show_path = False  # Откатываем флаг обратно
                    return
                # ----------------------

                # Очищаем старый путь
                for row in self.grid.matrix:
                    for cell in row:
                        cell.is_solution = False

                # Красим новый путь
                for x, y in result.path_coords:
                    self.grid.matrix[y][x].is_solution = True
            else:
                self._stub_action("Start or Exit point is missing!", command)
                self.gfx.show_path = False
                return

        # 3. Перерисовываем UI и лабиринт
        self._update_menu_line_smart(command, redraw_grid=True)
