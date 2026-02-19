# def _print_menu(self, is_path_visible: bool,
#                      char_style: str,
#                      color_style: str) -> None:
#         path_action = "Hide" if is_path_visible else "Show"
#
#         print(f"{self.title}")
#         print(f"[{self.CMD_GENERATE_NEW}] Generate new maze")
#         print(f"[{self.CMD_SHOW_PATH}] {path_action} path")
#         print(f"[{self.CMD_CHAR_STYLE}] Change characters stile. Now: {char_style})")
#         print(f"[{self.CMD_CHANGE_COLORS}] Change color stile. Now: {color_style})")
#         print(f"[{self.CMD_EXIT}] Quit program")
#
#
#        iterations = self.grid.grid_height * self.grid.grid_width * 10
#         if first_generation:
#             self.builder.init_vectors()
#             for i in range(iterations):
#                 self.builder.step()
#                 self.renderer.draw_cell()
#         else:

# from .grid import Grid
# import random
# import time
#
#
# class OriginShift:
#     def __init__(self, grid: Grid) -> None:
#         self.grid = grid
#         self.origin = None
#         self.deltas = {
#             "north": (0, -1),
#             "south": (0, 1),
#             "east": (1, 0),
#             "west": (-1, 0)
#         }
#         self.opposites = {
#             "north": "south",
#             "south": "north",
#             "east": "west",
#             "west": "east"
#         }
#
#     def init_vectors(self):
#         w, h = self.grid.grid_width, self.grid.grid_height
#
#         for row in self.grid.matrix:
#             for cell in row:
#                 cell.paths = {k: False for k in cell.paths}
#                 cell.vector = None
#
#         sx = (w - 7) // 2
#         sy = (h - 5) // 2
#         overrides = {
#             # Внутри "4" (чаша) -> Вверх
#             (1, 0): "north", (1, 1): "north",
#             # Разрыв между "4" и "2" -> Вниз (Коллектор)
#             (3, 0): "south", (3, 1): "south",
#             (3, 2): "south", (3, 3): "south", (3, 4): "south",
#             # Внутри "2" -> Влево
#             (4, 1): "west", (5, 1): "west",
#             # Низ "4" -> Вниз
#             (0, 3): "south", (1, 3): "south", (0, 4): "south", (1, 4): "south",
#             # Хвост "2" -> Вниз
#             (5, 3): "south", (6, 3): "south"
#         }
#
#         # 4. Главный проход по сетке
#         for y in range(h):
#             for x in range(w):
#                 cell = self.grid.matrix[y][x]
#
#                 if cell.forbidden:
#                     continue
#
#                 # ВАЖНО: Правый нижний угол — это Сток (Origin)
#                 if x == w - 1 and y == h - 1:
#                     self.origin = cell
#                     cell.vector = None
#                     continue
#
#                 direction = None
#
#                 rel_pos = (x - sx, y - sy)
#                 if rel_pos in overrides:
#                     desired = overrides[rel_pos]
#                     if self._is_valid_move(x, y, desired):
#                         direction = desired
#
#                 if not direction:
#                     if self._is_valid_move(x, y, "east"):
#                         direction = "east"
#                     elif self._is_valid_move(x, y, "south"):
#                         direction = "south"
#                     elif self._is_valid_move(x, y, "north"):
#                         direction = "north"
#                     elif self._is_valid_move(x, y, "west"):
#                         direction = "west"
#
#                 if direction:
#                     self._set_vector(cell, direction)
#                 else:
#                     self.origin = cell
#                     cell.vector = None
#
#     def _set_vector(self, cell, direction: str):
#         """
#         Устанавливает вектор логически И открывает стены графически.
#         """
#         cell.vector = direction
#
#         cell.paths[direction] = True
#
#         dx, dy = self.deltas[direction]
#         neighbor = self.grid.matrix[cell.cell_y + dy][cell.cell_x + dx]
#
#         opposite_dir = self.opposites[direction]
#         neighbor.paths[opposite_dir] = True
#
#     def _is_valid_move(self, x, y, direction) -> bool:
#         """Проверка: можно ли из (x,y) шагнуть в direction?"""
#         dx, dy = self.deltas[direction]
#         nx, ny = x + dx, y + dy
#         if not (0 <= nx < self.grid.grid_width and
#                 0 <= ny < self.grid.grid_height):
#             return False
#         if self.grid.matrix[ny][nx].forbidden:
#             return False
#         return True
#
#     def _close_wall(self, cell, direction: str):
#         """
#         Физически закрывает стену (paths=False) между клеткой и соседом.
#         Используется перед тем, как изменить вектор клетки.
#         """
#         cell.paths[direction] = False
#
#         dx, dy = self.deltas[direction]
#         neighbor = self.grid.matrix[cell.cell_y + dy][cell.cell_x + dx]
#
#         opposite_dir = self.opposites[direction]
#         neighbor.paths[opposite_dir] = False
#
#     def _get_valid_neighbors(self, cell):
#         """Возвращает список (Cell, direction), к которым можно прокопаться"""
#         candidates = []
#
#         for direction, (dx, dy) in self.deltas.items():
#             nx, ny = cell.cell_x + dx, cell.cell_y + dy
#             if (0 <= nx < self.grid.grid_width and
#                     0 <= ny < self.grid.grid_height):
#                 neighbor = self.grid.matrix[ny][nx]
#                 if not neighbor.forbidden:
#                     candidates.append((neighbor, direction))
#         return candidates
#
#     def step(self) -> list:
#         updates = []
#
#         current_origin = self.origin
#         neighbors = self._get_valid_neighbors(current_origin)
#         if not neighbors:
#             return []
#
#         target, direction = random.choice(neighbors)
#
#         current_origin.visited = True
#         target.visited = True
#
#         if target.vector:
#             should_close = True
#
#             if not self.grid.perfection:
#                 if random.random() < 0.05:
#                     should_close = False
#
#             if should_close:
#                 dx, dy = self.deltas[target.vector]
#                 old_neighbor = self.grid.matrix[target.cell_y + dy][target.cell_x + dx]
#
#                 self._close_wall(target, target.vector)
#
#                 updates.append(old_neighbor)
#
#         self._set_vector(current_origin, direction)
#         target.vector = None
#         self.origin = target
#
#         updates.append(current_origin)
#         updates.append(target)
#
#         return updates

# Note: These imports are based on the provided file content.
# Ensure these modules exist in your project structure.
from .builder import OriginShift
# from .dfs_backtracker import DFSBacktracker
# from .generators import GeneratorRegistry
from .grid import Grid
from .graphics import Graphics
# from .kruskal_generator import KruskalGenerator
from .maze_config import MazeConfig
from .menu import Menu
# from .mlx_viewer import MlxViewer
# from .prim_generator import PrimGenerator
from .renderer import Renderer
# from .solver import Solver
# from .writer import MazeWriter
#
# """
# The central controller for the A-Maze-Ing application.
# """
#
# from __future__ import annotations
#
# import sys
# import time
# from typing import Tuple, Union, Optional
#
# from .builder import OriginShift, DFSBuilder
# from .generators import GeneratorRegistry
# from .grid import Grid
# from .graphics import Graphics
# from .maze_config import MazeConfig
# from .menu import Menu
# from .renderer import Renderer
#
# # Type aliases for clarity
# Coord = Tuple[int, int]
# Cmd = Union[int, str, None]
#
#
# class Manager:
#     """Application controller: coordinates generation, rendering, and IO.
#
#     This class acts as the "brain" of the application (Controller pattern).
#     It binds together the Data Model (Grid), the View (Renderer/Graphics),
#     and the Business Logic (Generators/Solver). It handles the main event loop
#     and processes user commands.
#     """
#
#     def __init__(self, config: MazeConfig) -> None:
#         """Initializes the Manager and all core components."""
#         self.config = config
#
#         self.grid = Grid(config)
#         self.gfx = Graphics()
#         self.menu = Menu()
#         self.renderer = Renderer(self.gfx, self.menu)
#
#         # Инициализируем реестр генераторов (паттерн Стратегия)
#         self.registry = GeneratorRegistry(
#             generators={
#                 "origin_shift": OriginShift(self.grid),
#                 "dfs_backtracker": DFSBuilder(self.grid)
#             },
#             order=("origin_shift", "dfs_backtracker")
#         )
#
#         self.is_path_visible = False
#
#     def run(self):
#         """Starts the main application loop."""
#         # Передаем имя текущего генератора для начальной отрисовки меню
#         self.renderer.render_all(self.grid, self.registry.current().name)
#
#         while True:
#             try:
#                 command = self.menu.get_user_choice()
#             except ValueError:
#                 continue
#
#             match command:
#                 case self.menu.CMD_EXIT:
#                     self._handle_exit()
#
#                 case self.menu.CMD_GENERATE_NEW:
#                     self._handle_generate(command)
#
#                 case self.menu.CMD_SHOW_PATH:
#                     self._handle_unknown(command)
#
#                 case self.menu.CMD_CHAR_STYLE:
#                     self.gfx.toggle_style()
#                     # Обновляем строку 3 и ПЕРЕРИСОВЫВАЕМ лабиринт
#                     self._update_menu_line_smart(command, line_index=3, redraw_grid=True)
#
#                 case self.menu.CMD_CHANGE_COLORS:
#                     self.gfx.toggle_theme()
#                     # Обновляем строку 4 и ПЕРЕРИСОВЫВАЕМ лабиринт
#                     self._update_menu_line_smart(command, line_index=4, redraw_grid=True)
#
#                 case self.menu.CMD_CHANGE_GENERATOR:
#                     self.registry.next()
#                     # Обновляем строку 5, но лабиринт НЕ ТРОГАЕМ
#                     self._update_menu_line_smart(command, line_index=5, redraw_grid=False)
#
#                 case _:
#                     self._handle_unknown(command)
#
#     def _handle_exit(self):
#         """Handles the application exit sequence."""
#         self._stub_action("Hasta la vista, baby.", 5)
#         self.renderer.clear_screen()
#         sys.exit(0)
#
#     def _handle_generate(self, command: int):
#         """Orchestrates the maze generation workflow with animation."""
#         prompt_len = len(self.menu.get_choice()) + len(str(command))
#         sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
#         self.renderer.backspace(len(str(command)))
#
#         # 1. Получаем текущий выбранный алгоритм из реестра
#         builder = self.registry.current()
#
#         # 2. Подготавливаем сетку (единый интерфейс)
#         builder.setup()
#
#         self.renderer.save_cursor()
#         self.renderer.redraw_grid(self.grid)
#
#         total_cells = self.grid.grid_width * self.grid.grid_height
#         iterations = total_cells * 10
#
#         # 3. Крутим цикл анимации, пока алгоритм не вернет пустой список
#         for _ in range(iterations):
#             changed_cells = builder.step()
#
#             if not changed_cells:
#                 break
#
#             for cell in changed_cells:
#                 self.renderer.draw_cell(cell, delay=0.005)
#
#         self.renderer.restore_cursor()
#
#     def _update_menu_line_smart(self, command: int, line_index: int, redraw_grid: bool):
#         """Точечно обновляет одну строку меню и (опционально) сетку."""
#         cmd_str = str(command)
#         prompt_len = len(self.menu.get_choice()) + len(cmd_str)
#
#         # Стираем введенную пользователем команду
#         sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
#         self.renderer.backspace(len(cmd_str))
#
#         self.renderer.save_cursor()
#
#         # Обновляем нужную строку.
#         # Внимание: убедись, что метод update_menu_line в renderer.py
#         # принимает gen_name, как мы обсуждали ранее!
#         self.renderer.update_menu_line(
#             self.grid.grid_height,
#             line_index,
#             self.registry.current().name
#         )
#
#         # Перерисовываем сетку, только если изменилась графика
#         if redraw_grid:
#             self.renderer.redraw_grid(self.grid)
#
#         self.renderer.restore_cursor()
#
#     def _handle_unknown(self, command: Cmd):
#         self._stub_action("Unknown command", command)
#
#     def _stub_action(self, message: str, command: Cmd):
#         """Displays a temporary status message."""
#         command_len = 1 if isinstance(command, int) else len(str(command))
#
#         msg_y = self.grid.grid_height + len(self.menu.menu_list) + 2
#         full_message = f">>> {message}"
#
#         self.renderer.move_cursor(1, msg_y)
#         sys.stdout.write("\033[K")
#         self.renderer.type_text(full_message)
#         sys.stdout.flush()
#
#         time.sleep(3)
#
#         self.renderer.backspace(len(full_message))
#         outset = len(self.menu.get_choice()) + 1 + command_len
#         self.renderer.move_cursor(outset, msg_y - 1)
#         self.renderer.backspace(command_len)
#         sys.stdout.flush()

"""
Handles all terminal output and visual rendering logic.
"""

import random
import sys
import time

from .grid import Grid
from .cell import Cell
from .menu import Menu
from .graphics import Graphics


class Renderer:
    """Orchestrates the visualization of the maze and UI components.

    This class serves as an abstraction layer for terminal manipulation.
    It handles cursor movement, screen clearing, text typing effects, and
    delegates specific character/color choices to the Graphics module.

    Attributes:
        gfx (Graphics): Reference to the graphics module for style/theme data.
        menu (Menu): Reference to the menu module for UI text generation.
    """

    def __init__(self, grafix_module: Graphics, menu_module: Menu) -> None:
        """Initializes the Renderer.

        Args:
            grafix_module (Graphics): Instance handling visual styles.
            menu_module (Menu): Instance handling menu text logic.
        """
        self.gfx = grafix_module
        self.menu = menu_module

    @staticmethod
    def clear_screen() -> None:
        """Clears the entire terminal screen and moves cursor to home (0,0)."""
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    @staticmethod
    def hide_cursor() -> None:
        """Hides the terminal cursor to prevent flickering during rendering."""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_cursor() -> None:
        """Restores the terminal cursor visibility."""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def save_cursor() -> None:
        """Saves the current cursor position in the terminal memory."""
        sys.stdout.write("\0337")
        sys.stdout.flush()

    @staticmethod
    def restore_cursor() -> None:
        """Restores the cursor to the previously saved position."""
        sys.stdout.write("\0338")
        sys.stdout.flush()

    @staticmethod
    def move_cursor(x: int, y: int) -> None:
        """Moves the cursor to specific coordinates.

        Args:
            x (int): Column number (1-based index).
            y (int): Row number (1-based index).
        """
        sys.stdout.write(f"\033[{y};{x}H")

    @staticmethod
    def type_text(text: str, min_delay: float = 0.04,
                  max_delay: float = 0.06) -> None:
        """Prints text character by character to simulate typing."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(random.uniform(min_delay, max_delay))

    @staticmethod
    def backspace(count: int, min_delay: float = 0.04,
                  max_delay: float = 0.09) -> None:
        """Simulates pressing backspace to erase characters."""
        for _ in range(count):
            sys.stdout.write("\b \b")
            sys.stdout.flush()
            time.sleep(random.uniform(min_delay, max_delay))

    def draw_cell(self, cell: Cell, delay: float = 0.02) -> None:
        """Renders a single cell at its calculated screen position."""
        screen_y = cell.cell_y + 1
        screen_x = cell.cell_x + 1

        char = self.gfx.get_char_for_cell(cell)
        color = self.gfx.get_color_for_cell(cell)
        reset = self.gfx.current_theme_map["RESET"]

        self.move_cursor(screen_x, screen_y)
        sys.stdout.write(f"{color}{char}{reset}")
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)

    def redraw_grid(self, grid: Grid) -> None:
        """Refreshes the entire maze grid visualization."""
        self.hide_cursor()
        for row in grid.matrix:
            for cell in row:
                self.draw_cell(cell, 0)
        self.show_cursor()

    # --- ИЗМЕНЕНИЯ НАЧИНАЮТСЯ ЗДЕСЬ ---

    def update_menu_line(self, maze_height: int, line_index: int, gen_name: str) -> None:
        """Updates a specific line in the menu section below the maze.

        Args:
            maze_height (int): Used to calculate the Y-offset (below the maze).
            line_index (int): The index of the menu line to update.
            gen_name (str): The name of the currently active generator.
        """
        current_y = maze_height + 2 + line_index

        # Добавили gen_name=gen_name
        menu_list = self.menu.get_current_list(
            path_visible=self.gfx.show_path,
            char_style=self.gfx.current_style_name,
            color_style=self.gfx.current_theme_name,
            gen_name=gen_name
        )
        text = menu_list[line_index]
        self.move_cursor(1, current_y)
        sys.stdout.write("\033[K")
        self.type_text(text)
        sys.stdout.flush()

    def render_all(self, grid: Grid, gen_name: str) -> None:
        """Renders the entire application interface (Grid + Menu).

        Args:
            grid (Grid): The maze grid to render.
            gen_name (str): The name of the currently active generator.
        """
        self.clear_screen()

        # Добавили gen_name=gen_name
        menu_list = self.menu.get_current_list(
            path_visible=self.gfx.show_path,
            char_style=self.gfx.current_style_name,
            color_style=self.gfx.current_theme_name,
            gen_name=gen_name
        )

        # Draw Grid
        for row in grid.matrix:
            for cell in row:
                self.draw_cell(cell, 0)  # Убрал задержку для быстрой отрисовки базы

        # Spacer
        self.move_cursor(1, grid.grid_height + 1)
        print(" " * grid.grid_width)

        # Draw Menu (передаем gen_name в update_menu_line)
        for i in range(len(menu_list)):
            self.update_menu_line(grid.grid_height, i, gen_name)

        self.show_cursor()