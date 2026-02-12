import sys
from pathlib import Path
from classes import MazeConfig, Cell, Grid, Graphics, Renderer, Menu

BASE_DIR = Path(__file__).resolve().parent


def main():
    if len(sys.argv) == 2:
        con_file_name = sys.argv[1]
        full_config_path = BASE_DIR / con_file_name
        configs = MazeConfig.load_config(full_config_path)

        grid = Grid(configs.maze_width, configs.maze_height)
        grap = Graphics()
        menu = Menu()
        rend = Renderer(grap, menu)
        rend.render_all(grid)
        print()
        menu.get_user_choice()



if __name__ == "__main__":
    main()
