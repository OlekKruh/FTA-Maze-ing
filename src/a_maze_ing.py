"""
Main entry point for the A-Maze-ing application.

This script handles command-line arguments, resolves the configuration
file path, initializes the application manager, and provides graceful
error handling to prevent unexpected crashes.
"""

import sys
from pathlib import Path

from mazegen import MazeConfig, Manager

BASE_DIR = Path(__file__).resolve().parent


def main() -> None:
    """
    Execute the main application flow.

    Validates command-line arguments, locates and parses the
    configuration file, and runs the Manager.
    Catches KeyboardInterrupt and general exceptions
    to ensure graceful termination.
    """
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    con_file_name = sys.argv[1]

    # Resolve config path: check current working directory
    # first, then script directory
    cwd_path = Path(con_file_name)
    if cwd_path.is_file():
        full_config_path = cwd_path.resolve()
    else:
        full_config_path = (BASE_DIR / con_file_name).resolve()
    try:
        configs = MazeConfig.load_config(full_config_path)
        app = Manager(configs)
        app.run()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print("\nCritical Error: An unexpected issue "
              "occurred during execution.")
        print(f"Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
