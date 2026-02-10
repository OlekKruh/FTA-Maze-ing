from .cell import Cell
from typing import List

class Grid:
    matrix = []

    def __init__(self, grid_width: int, grid_height: int) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.matrix = [
            [Cell(x, y) for x in range(self.grid_width)]
            for y in range(self.grid_height)
        ]

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

    def display(self):
        """
        Метод специально для быстрой проверки структуры в консоли
        """
        for row in self.matrix:
            print(" ".join([f"[ ]" for _ in row]))

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