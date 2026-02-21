"""
Configuration management for the maze generation application.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any


class MazeConfig:
    """Holds configuration settings for maze generation.

    This class handles loading settings from external files,
     validating the data, and providing a structured object
     to access configuration parameters like
     dimensions, entry/exit points, and algorithm constraints.

    Attributes:
        maze_width (int): The width of the maze grid.
        maze_height (int): The height of the maze grid.
        maze_entry (List[int]): Coordinates [x, y] for the starting point.
        maze_exit (List[int]): Coordinates [x, y] for the exit point.
        output_file (str): Filename for saving the generated maze.
        maze_perfect (bool): If True, generates a perfect maze (no loops).
    """

    KEY_MAPPING: Dict[str, str] = {
        "WIDTH": "maze_width",
        "HEIGHT": "maze_height",
        "ENTRY": "maze_entry",
        "EXIT": "maze_exit",
        "OUTPUT_FILE": "output_file",
        "PERFECT": "perfect"
    }

    def __init__(self, maze_width: int, maze_height: int,
                 maze_entry: List[int], maze_exit: List[int],
                 output_file: str, perfect: bool) -> None:
        """Initializes a MazeConfig instance.

        Args:
            maze_width (int): Width of the maze.
            maze_height (int): Height of the maze.
            maze_entry (List[int]): [x, y] coordinates for start.
            maze_exit (List[int]): [x, y] coordinates for exit.
            output_file (str): Output filename.
            perfect (bool): Loop generation flag.
        """
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height
        self.maze_entry: List[int] = maze_entry
        self.maze_exit: List[int] = maze_exit
        self.output_file: str = output_file
        self.maze_perfect: bool = perfect

    def get_info(self) -> str:
        """Returns a string representation of the configuration.

        Returns:
            str: Dictionary string of instance attributes.
        """
        return str(self.__dict__)

    @classmethod
    def load_config(cls, user_file_path: Path) -> "MazeConfig":
        """Attempts to load configuration from a file.

        Args:
            user_file_path (Path): Path to the user-provided config file.

        Returns:
            MazeConfig: An initialized configuration object.

        Raises:
            SystemExit: If the file is not found, unreadable, or contains
                invalid configuration parameters.
        """
        if not user_file_path.is_file():
            print(f"Error: Configuration file '{user_file_path}' not found.")
            sys.exit(1)

        raw_data: Dict[str, Any] = cls._read_file(user_file_path)
        if not raw_data:
            print(f"Error: Cannot read data or file is"
                  f" empty '{user_file_path}'.")
            sys.exit(1)

        if cls._config_verify(raw_data):
            return cls(**raw_data)
        else:
            print(f"Error: Data validation failed for '{user_file_path}'.")
            sys.exit(1)

    @classmethod
    def _read_file(cls, file_path: Path) -> Dict[str, Any]:
        """Parses a configuration file.

        Reads line by line, splitting by '='. Converts values to appropriate
        types (int, list, bool) based on the content.

        Args:
            file_path (Path): Path to the file to read.

        Returns:
            Dict[str, Any]: A dictionary of parsed configuration data with
            mapped keys. Returns an empty dict on failure.
        """
        data: Dict[str, Any] = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        raw_key, value = line.strip().split("=", 1)
                        value = value.strip()

                        if raw_key not in cls.KEY_MAPPING:
                            continue

                        key: str = cls.KEY_MAPPING[raw_key]

                        if "," in value:
                            data[key] = [int(x) for x in value.split(",")]
                        elif value.isdigit():
                            data[key] = int(value)
                        elif value.lower() == "false":
                            data[key] = False
                        elif value.lower() == "true":
                            data[key] = True
                        else:
                            data[key] = value
            return data
        except Exception as e:
            print(f"Exception while reading {file_path}: {e}")
            return {}

    @staticmethod
    def _config_verify(data: Dict[str, Any]) -> bool:
        """Validates that the parsed data contains all required fields.

        Also verifies that the entry and exit coordinates fit within
        the specified maze dimensions to prevent out-of-bounds crashes.

        Args:
            data (Dict[str, Any]): The dictionary parsed from the file.

        Returns:
            bool: True if data is valid, False otherwise.
        """
        required: set[str] = {"maze_width", "maze_height", "maze_entry",
                              "maze_exit", "output_file", "perfect"}

        if not data or not required.issubset(data.keys()):
            missing = required - data.keys()
            print(f"Validation error: Missing keys {missing}")
            return False

        for key in required:
            value: Any = data[key]
            if value is None:
                print(f"Validation error: key '{key}' contains None")
                return False
            if isinstance(value, str) and value.strip() == "":
                print(f"Validation error: key '{key}' contains empty string")
                return False
            if isinstance(value, list) and len(value) == 0:
                print(f"Validation error: key '{key}' contains empty list")
                return False

        width: int = data["maze_width"]
        height: int = data["maze_height"]

        if width < 3 or height < 3:
            print(f"Validation error: Maze dimensions must"
                  f" be at least 3x3. Got {width}x{height}.")
            return False

        entry: List[int] = data["maze_entry"]
        exit_pt: List[int] = data["maze_exit"]

        if isinstance(entry, list) and len(entry) >= 2:
            if not (0 <= entry[0] < width and 0 <= entry[1] < height):
                print(f"Validation error: ENTRY {entry} is "
                      f"out of bounds for a {width}x{height} maze.")
                return False

        if isinstance(exit_pt, list) and len(exit_pt) >= 2:
            if not (0 <= exit_pt[0] < width and 0 <= exit_pt[1] < height):
                print(f"Validation error: EXIT {exit_pt} is out of"
                      f" bounds for a {width}x{height} maze.")
                return False

        return True
