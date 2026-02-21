"""
Exports the generated maze to a text file in a 16-bit (hexadecimal) format.
"""

from .grid import Grid
from .cell import Cell


class MazeWriter:
    """Handles saving the maze state and solution to a file."""

    # Битовые значения для каждого направления (N=1, E=2, S=4, W=8)
    _MASKS = {
        "north": 1,
        "east": 2,
        "south": 4,
        "west": 8
    }

    @staticmethod
    def _cell_to_hex(cell: Cell) -> str:
        """Converts cell passages into a single hex character (0-F)."""
        if cell.forbidden:
            return "F"

        value = 0
        for direction, is_open in cell.paths.items():
            if not is_open:
                value += MazeWriter._MASKS[direction]

        return f"{value:X}"

    @classmethod
    def export_to_file(cls, grid: Grid, path_dirs: str, filename: str) -> None:
        """Writes the hex grid, coordinates, and path string to the target file."""
        start_coord = (0, 0)
        exit_coord = (0, 0)

        # Писатель сам ищет старт и финиш по флагам внутри клеток
        for row in grid.matrix:
            for cell in row:
                if cell.is_start:
                    start_coord = (cell.cell_x, cell.cell_y)
                elif cell.is_exit:
                    exit_coord = (cell.cell_x, cell.cell_y)

        # Открываем файл на запись и формируем структуру как на твоем скриншоте
        with open(filename, 'w', encoding='utf-8') as f:
            # 1. Записываем саму сетку (каждая строка лабиринта - это строка hex-символов)
            for row in grid.matrix:
                line = "".join(cls._cell_to_hex(cell) for cell in row)
                f.write(line + "\n")

            f.write("\n")

            f.write(f"{start_coord[0]},{start_coord[1]}\n")
            f.write(f"{exit_coord[0]},{exit_coord[1]}\n")

            f.write(f"{path_dirs}\n")
