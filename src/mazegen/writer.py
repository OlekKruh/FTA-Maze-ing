"""
Exports the generated maze to a text file in a 16-bit (hexadecimal) format.
"""

from typing import Dict, Tuple

from .grid import Grid
from .cell import Cell


class MazeWriter:
    """Handles saving the maze state and solution to a file.

    This class encapsulates the logic for converting the grid into a
    standardized format where each cell's walls are represented by a
    single hexadecimal character based on a bitwise mask.

    Attributes:
        _MASKS (Dict[str, int]): Bit values for each wall direction
            (North=1, East=2, South=4, West=8).
    """

    _MASKS: Dict[str, int] = {
        "north": 1,
        "east": 2,
        "south": 4,
        "west": 8
    }

    @staticmethod
    def _cell_to_hex(cell: Cell) -> str:
        """Converts cell walls into a single hex character (0-F).

        Calculates a 4-bit integer based on the presence of walls
        (where True means a wall exists) and returns its uppercase
        hexadecimal representation. Forbidden cells are completely
        walled off ('F').

        Args:
            cell (Cell): The cell to evaluate.

        Returns:
            str: A single uppercase hexadecimal character.
        """
        if cell.forbidden:
            return "F"

        value: int = 0
        for direction, is_open in cell.paths.items():
            if not is_open:
                value += MazeWriter._MASKS[direction]

        return f"{value:X}"

    @classmethod
    def export_to_file(cls, grid: Grid, path_dirs: str, filename: str) -> None:
        """Writes the hex grid, coordinates, and path string to a file.

        Scans the grid to locate the precise entry and exit coordinates,
        formats the maze row by row into hex strings, and appends the
        solution path at the bottom.

        Args:
            grid (Grid): The maze grid object to export.
            path_dirs (str): The string of directions solving the maze.
            filename (str): The target file path for the export.
        """
        start_coord: Tuple[int, int] = (0, 0)
        exit_coord: Tuple[int, int] = (0, 0)

        for row in grid.matrix:
            for cell in row:
                if cell.is_start:
                    start_coord = (cell.cell_x, cell.cell_y)
                elif cell.is_exit:
                    exit_coord = (cell.cell_x, cell.cell_y)

        with open(filename, 'w', encoding='utf-8') as f:
            for row in grid.matrix:
                line: str = "".join(cls._cell_to_hex(cell) for cell in row)
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{start_coord[0]},{start_coord[1]}\n")
            f.write(f"{exit_coord[0]},{exit_coord[1]}\n")
            f.write(f"{path_dirs}\n")
