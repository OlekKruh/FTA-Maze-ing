from . import Cell, MazeConfig
from typing import List


class Grid:
    matrix = []

    def __init__(self, config: MazeConfig) -> None:
        self.grid_width = config.maze_width
        self.grid_height = config.maze_height
        self.matrix = [
            [Cell(x, y) for x in range(self.grid_width)]
            for y in range(self.grid_height)
        ]
        start_x, start_y = config.maze_entry
        exit_x, exit_y = config.maze_exit

        # Назначаем свойства напрямую
        self.matrix[start_y][start_x].is_start = True
        self.matrix[exit_y][exit_x].is_exit = True

    def __getitem__(self, item: tuple[int, int]) -> Cell:
        """
        Y(строка), X(столбец), особенности работы с выводом текста
        сначала выбор строки потом выбор элемента в строке(столбца)
        """
        x, y = item
        return self.matrix[y][x]

    def __repr__(self) -> str:
        """
        Лаконичная информация для логов
        """
        return (f"Grid = {self.grid_width}x{self.grid_height}\n"
                f"Cells = {self.grid_width * self.grid_height}")

    # def display(self):
    #     """
    #     Метод специально для быстрой проверки структуры в консоли
    #     """
    #     for row in self.matrix:
    #         print(" ".join([f"[ ]" for _ in row]))

    def get_neighbors(self, item: tuple[int, int]) -> List[Cell]:
        x, y = item
        neighbors = []

        direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.grid_width and 0 <= ny <= self.grid_height:
                neighbors.append(self[nx, ny])
        return neighbors

    def get_info(self) -> str:
        return str(self.__dict__)
