from typing import Dict


class Cell:
    def __init__(self, cell_x: int, cell_y: int) -> None:
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.passage = {
            "north": True,
            "east": True,
            "south": True,
            "west": True,
        }
        self.is_start = False
        self.is_exit = False
        self.visited = False
        self.forbidden = False

    def get_info(self) -> str:
        return str(self.__dict__)

    def set_path(self, direction: str, is_path: bool) -> None:
        if direction in self.passage:
            self.passage[direction] = is_path
