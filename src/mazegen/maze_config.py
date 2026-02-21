"""
Configuration management for the maze generation application.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any


class MazeConfig:
    """Holds configuration settings for maze generation."""

    KEY_MAPPING = {
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
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze_entry = maze_entry
        self.maze_exit = maze_exit
        self.output_file = output_file
        self.maze_perfect = perfect

    @classmethod
    def load_config(cls, user_file_path: Path) -> "MazeConfig":
        """Attempts to load configuration from the specified file."""

        # 1. Если файла нет - сразу выходим, никаких скрытых подмен!
        if not user_file_path.is_file():
            print(f"Error: Configuration file '{user_file_path}' not found.")
            sys.exit(1)

        raw_data = cls._read_file(user_file_path)
        if not raw_data:
            print(f"Error: Cannot read data or file "
                  f"is empty '{user_file_path}'.")
            sys.exit(1)

        # 2. Проверяем валидность данных
        if cls._config_verify(raw_data):
            return cls(**raw_data)
        else:
            print(f"Error: Data validation failed for '{user_file_path}'.")
            sys.exit(1)

    @classmethod
    def _read_file(cls, file_path: Path) -> Dict[str, Any]:
        """Parses a configuration file."""
        data = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        raw_key, value = line.strip().split("=", 1)
                        value = value.strip()

                        if raw_key not in cls.KEY_MAPPING:
                            continue

                        key = cls.KEY_MAPPING[raw_key]

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
        """Validates that the parsed data contains all required
        fields and logical bounds.
        """
        required = {"maze_width", "maze_height", "maze_entry",
                    "maze_exit", "output_file", "perfect"}

        if not data or not required.issubset(data.keys()):
            missing = required - data.keys()
            print(f"Validation error: Missing keys {missing}")
            return False

        # Базовые проверки на пустоту (твои старые проверки)
        for key in required:
            value = data[key]
            if value is None:
                print(f"Validation error: key '{key}' contains None")
                return False
            if isinstance(value, str) and value.strip() == "":
                print(f"Validation error: key '{key}' contains empty string")
                return False
            if isinstance(value, list) and len(value) == 0:
                print(f"Validation error: key '{key}' contains empty list")
                return False

        # --- НОВАЯ ЗАЩИТА ОТ КРАШЕЙ (impossible maze parameters) ---
        width = data["maze_width"]
        height = data["maze_height"]
        entry = data["maze_entry"]
        exit_pt = data["maze_exit"]

        if isinstance(entry, list) and len(entry) >= 2:
            if not (0 <= entry[0] < width and 0 <= entry[1] < height):
                print(f"Validation error: ENTRY {entry} is out of bounds "
                      f"for a {width}x{height} maze.")
                return False

        if isinstance(exit_pt, list) and len(exit_pt) >= 2:
            if not (0 <= exit_pt[0] < width and 0 <= exit_pt[1] < height):
                print(f"Validation error: EXIT {exit_pt} is out of bounds "
                      f"for a {width}x{height} maze.")
                return False

        return True
