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
        x, y = item
        return self.matrix[x][y]

    def get_neighbors(self, item: tuple[int, int]) -> List[Cell]:
        x, y = item
        neighbors = []

        direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.grid_width and 0 <= ny <= self.grid_height:
                neighbors.append(self[nx, ny])
        return neighbors
