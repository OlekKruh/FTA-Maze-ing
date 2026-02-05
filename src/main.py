import sys
from src.classes import MazeConfig


def main():
    if len(sys.argv) == 1:
        con_file_name = sys.argv[1]
        configs = MazeConfig.load_config(con_file_name)


if __name__ == "__main__":
    main()
