from typing import List, Dict


class MazeConfig:
    DEFAULT_CONFIG_NAME = "default_config.txt"

    def __init__(self, maze_width: int, maze_height: int,
                 maze_entry: List[int], maze_exit: List[int],
                 output_file_name: str, maze_perfect: bool):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze_entry = maze_entry
        self.maze_exit = maze_exit
        self.output_file_name = output_file_name
        self.maze_perfect = maze_perfect

    @classmethod
    def load_config(cls, file_name=None) -> Dict:
        ...

    @staticmethod
    def _read_file(self):
        ...

    @staticmethod
    def _config_verify(self):
        ...
