class Cell:
    def __init__(self, cell_x: int, cell_y: int) -> None:
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.paths = {
            "north": False,
            "east": False,
            "south": False,
            "west": False,
        }
        self.is_start = False  # условие определения
        self.is_exit = False  # условие определения
        self.visited = False  # условие определения
        self.forbidden = False  # условие определения
        self.is_solution = False  # условие определения

    def get_info(self) -> str:
        return str(self.__dict__)

    def set_path(self, direction: str, is_path: bool) -> None:
        if direction in self.paths:
            self.paths[direction] = is_path
