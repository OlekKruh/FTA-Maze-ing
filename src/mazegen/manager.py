"""
The central controller for the A-Maze-Ing application.
"""

from __future__ import annotations

import sys
import time
from typing import Tuple, Union, Optional

from .builder import (BaseBuilder, OriginShift,
                      DFSBuilder, PrimBuilder, KruskalBuilder)
from .generators import GeneratorRegistry
from .grid import Grid
from .graphics import Graphics
from .maze_config import MazeConfig
from .menu import Menu
from .renderer import Renderer
from .solver import Solver
from .writer import MazeWriter

# Type aliases for clarity
Coord = Tuple[int, int]
Cmd = Union[int, str, None]


class Manager:
    """Application controller: coordinates generation, rendering, and IO.

    This class acts as the orchestrator. It initializes the UI components,
    handles the main application loop, processes user input, and delegates
    tasks to the respective Builder, Solver, and Renderer components.

    Attributes:
        config (MazeConfig): The configuration parameters for the maze.
        grid (Grid): The underlying data structure of the maze.
        gfx (Graphics): The graphics engine managing styles and colors.
        menu (Menu): The menu component for user interaction.
        renderer (Renderer): The engine responsible for terminal output.
        registry (GeneratorRegistry): The strategy manager for algorithms.
        is_path_visible (bool): Tracks if the solution path should be rendered.
    """

    def __init__(self, config: MazeConfig) -> None:
        """Initializes the Manager with all necessary subsystems.

        Args:
            config (MazeConfig): Configuration object containing dimensions
                and generation parameters.
        """
        self.config: MazeConfig = config

        self.grid: Grid = Grid(config)
        self.gfx: Graphics = Graphics()
        self.menu: Menu = Menu()
        self.renderer: Renderer = Renderer(self.gfx, self.menu)

        self.registry: GeneratorRegistry = GeneratorRegistry(
            generators={
                "origin_shift": OriginShift(self.grid),
                "dfs_backtracker": DFSBuilder(self.grid),
                "prim": PrimBuilder(self.grid),
                "kruskal": KruskalBuilder(self.grid)
            },
            order=("origin_shift", "dfs_backtracker", "prim", "kruskal")
        )
        self.is_path_visible: bool = False

    def run(self) -> None:
        """Starts the main application loop.

        Renders the initial screen and enters an infinite loop to process
        user commands until the exit command is received.
        """
        self.renderer.render_all(self.grid,
                                 self.registry.current().name)
        while True:
            try:
                command: Cmd = self.menu.get_user_choice()
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

    def _handle_exit(self) -> None:
        """Handles the application exit sequence.

        Displays a farewell message, clears the terminal screen,
        and terminates the program.
        """
        self._stub_action("Hasta la vista, baby.", 5)
        self.renderer.clear_screen()
        sys.exit(0)

    def _handle_generate(self, command: Cmd) -> None:
        """Generates a new maze using the currently selected algorithm.

        Executes the generation step-by-step to provide terminal animation,
        then automatically exports the final result.

        Args:
            command (Cmd): The user command that triggered the generation.
        """
        prompt_len: int = len(self.menu.get_choice()) + len(str(command))
        sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
        self.renderer.backspace(len(str(command)))

        builder: BaseBuilder = self.registry.current()
        builder.setup()

        self.renderer.save_cursor()
        self.renderer.redraw_grid(self.grid)

        total_cells: int = self.grid.grid_width * self.grid.grid_height
        iterations: int = total_cells * 10

        for _ in range(iterations):
            changed_cells = builder.step()

            if not changed_cells:
                break

            for cell in changed_cells:
                self.renderer.draw_cell(cell, delay=0.005)

        self.renderer.restore_cursor()
        self._export_maze_in_background()

    def _handle_unknown(self, command: Cmd) -> None:
        """Displays an error message for unrecognized commands.

        Args:
            command (Cmd): The unrecognized input provided by the user.
        """
        self._stub_action("Unknown command", command)

    def _update_menu_line_smart(self, command: int, redraw_grid: bool) -> None:
        """Updates the menu line dynamically without flickering.

        Args:
            command (int): The last command executed.
            redraw_grid (bool): Whether the entire grid needs to be redrawn
                (e.g., when a color theme changes).
        """
        cmd_str: str = str(command)
        prompt_len: int = len(self.menu.get_choice()) + len(cmd_str)

        sys.stdout.write(f"\033[A\033[G\033[{prompt_len}C")
        self.renderer.backspace(len(cmd_str))

        self.renderer.save_cursor()

        self.renderer.update_menu_line(
            self.grid.grid_height,
            command, self.registry.current().name)

        if redraw_grid:
            self.renderer.redraw_grid(self.grid)

        self.renderer.restore_cursor()

    def _stub_action(self, message: str, command: Cmd) -> None:
        """Displays a temporary notification message on the screen.

        Args:
            message (str): The text message to display.
            command (Cmd): The command that triggered this action.
        """
        command_len: int = 1 if isinstance(command, int) else len(str(command))

        msg_y: int = self.grid.grid_height + len(self.menu.menu_list) + 2
        full_message: str = f">>> {message}"

        self.renderer.move_cursor(1, msg_y)
        sys.stdout.write("\033[K")
        self.renderer.type_text(full_message)
        sys.stdout.flush()

        time.sleep(2)

        self.renderer.backspace(len(full_message))
        outset: int = len(self.menu.get_choice()) + 1 + command_len
        self.renderer.move_cursor(outset, msg_y - 1)
        self.renderer.backspace(command_len)
        sys.stdout.flush()

    def _handle_show_path(self, command: int) -> None:
        """Toggles the solution path visibility and solves the maze if needed.

        Args:
            command (int): The user command that triggered the action.
        """
        # 1. Toggle visibility flag
        self.gfx.show_path = not self.gfx.show_path

        # 2. If visibility is enabled, search for the path
        if self.gfx.show_path:
            solver: Solver = Solver(self.grid)

            start_coord: Optional[Coord] = None
            exit_coord: Optional[Coord] = None

            for row in self.grid.matrix:
                for cell in row:
                    if cell.is_start:
                        start_coord = (cell.cell_x, cell.cell_y)
                    elif cell.is_exit:
                        exit_coord = (cell.cell_x, cell.cell_y)

            if start_coord and exit_coord:
                result = solver.solve(start_coord, exit_coord)

                if not result.path_coords:
                    self._stub_action(
                        "Path not found! Maze might be broken.",
                        command)
                    self.gfx.show_path = False
                    return

                # Clear old path
                for row in self.grid.matrix:
                    for cell in row:
                        cell.is_solution = False

                # Paint the new path
                for x, y in result.path_coords:
                    self.grid.matrix[y][x].is_solution = True
            else:
                self._stub_action("Start or Exit point is missing!", command)
                self.gfx.show_path = False
                return

        # 3. Redraw the UI and the grid
        self._update_menu_line_smart(command, redraw_grid=True)

    def _export_maze_in_background(self) -> None:
        """Silently solves the generated maze and exports it to a file.

        This method identifies the entry and exit, runs the BFS solver
        to get the sequence of directions, and delegates the file
        writing to the MazeWriter.
        """
        start_coord: Optional[Coord] = None
        exit_coord: Optional[Coord] = None

        # 1. Find start and exit points
        for row in self.grid.matrix:
            for cell in row:
                if cell.is_start:
                    start_coord = (cell.cell_x, cell.cell_y)
                elif cell.is_exit:
                    exit_coord = (cell.cell_x, cell.cell_y)

        # 2. If points exist, run Solver to get the path string
        path_dirs: str = ""
        if start_coord and exit_coord:
            solver: Solver = Solver(self.grid)
            result = solver.solve(start_coord, exit_coord)
            path_dirs = result.path_dirs

        # 3. Pass data to the Writer using the config filename
        MazeWriter.export_to_file(
            grid=self.grid,
            path_dirs=path_dirs,
            filename=self.config.output_file
        )
