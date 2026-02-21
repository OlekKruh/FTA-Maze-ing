*This project has been created as part of the 42 curriculum by ndemkiv, okruhlia.*

> [!WARNING]
> *The accuracy of the information or implementation may not correspond to reality.*
> ___USE AT YOUR OWN RISK!___

**Fabricated within the Data-Forges of:**

![Forge World Warsaw](https://img.shields.io/badge/Sector-42_Warsaw-b71c1c?style=for-the-badge&logo=42&logoColor=white)

**Sacred Tech-Stack (Lingua Technis):**

![Python](https://img.shields.io/badge/Lingua_Technis-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyCharm](https://img.shields.io/badge/Cogitator_Interface-PyCharm-000000?style=for-the-badge&logo=jetbrains&logoColor=white)

**Sustained by:**

![Recaf](https://img.shields.io/badge/Coffee_Stimulants-High_Grade-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white)
![&](https://img.shields.io/badge/-%26-gray?style=for-the-badge)
![Machine Spirit](https://img.shields.io/badge/Praise_the-Omnissiah-8B0000?style=for-the-badge&logo=warhammer&logoColor=white)

**Verification Rites:**

![Machine Spirit](https://img.shields.io/badge/Machine_Spirit-Appeased-success?style=for-the-badge&logo=robot-framework&logoColor=white)
> *"From the weakness of the mind, Omnissiah save us."*

---

# A-Maze-ing

## Description
A-Maze-ing is a highly customizable, terminal-based maze generator and solver written in Python. The project explores procedural content generation and graph theory to create fully connected mazes, guarantee a solvable path, and visually render the results directly in the terminal without flickering. It also features a built-in shortest-path solver and exports the maze data into a standardized 16-bit hexadecimal format.

## Instructions
**Prerequisites:** Python 3.10 or newer.

**Installation & Execution:**
We use a `Makefile` to automate the setup process.

1. Install dependencies and setup the virtual environment:

    make install

2. Run the application:

    make run

   *(Alternatively, run manually: `python3 src/a_maze_ing.py src/config.txt`)*

**Other Make commands:**
- `make build` - Packages the reusable `mazegen` module into `.whl` and `.tar.gz` archives.
- `make clean` - Removes the virtual environment, cache, build files, and generated packages.
- `make lint` - Runs `flake8` and `mypy` to check code quality.

## Configuration File Format
The program relies on a configuration file (e.g., `config.txt`) to define maze parameters. The file uses a simple `KEY=VALUE` format:
- `WIDTH` (int): Maze width (number of cells).
- `HEIGHT` (int): Maze height.
- `ENTRY` (x,y): Entry coordinates.
- `EXIT` (x,y): Exit coordinates.
- `OUTPUT_FILE` (string): Filename for saving the hex representation (e.g., `maze.txt`).
- `PERFECT` (True/False): If True, generates a perfect maze (one unique path).

## Algorithms Chosen
- **Origin Shift (Wilson's/Aldous-Broder concept):** Chosen to generate perfect mazes and specifically to carve out the mandatory "42" shape in the grid. It allows for controlled "flow" vectors and guarantees uniform spanning trees.
- **DFS (Depth-First Search) Backtracker:** Generates mazes with long, winding corridors and fewer dead ends.
- **Prim's Algorithm:** Creates highly branching mazes with many short, predictable cul-de-sacs.
- **Kruskal's Algorithm:** Uses a randomized disjoint-set data structure to build highly symmetric and fascinating perfect mazes.
- **BFS (Breadth-First Search) Solver:** Implemented to guarantee finding the shortest possible path from ENTRY to EXIT.

## Reusable Package (`mazegen`)
The core generation logic has been decoupled from the visualizer into a standalone package named `mazegen`.

**To install in another project:**
1. Run `make build` in our repository to generate the `.whl` file.
2. In your new project, run: `pip install path/to/mazegen-1.0.0-py3-none-any.whl`

**Usage Example:**

    from mazegen.maze_config import MazeConfig
    from mazegen.manager import Manager

    # Create a configuration object
    config = MazeConfig(20, 15, [0, 0], [19, 14], "out.txt", True)

    # Initialize and run the generator
    app = Manager(config)
    app.run()

## Team & Project Management
- **ndemkiv:** Authored a suite of maze generation algorithms (DFS, Prim's, Kruskal's), developed the BFS pathfinding solver logic, and managed the project infrastructure (Poetry, Makefile, packaging setup).
- **okruhlia:** Designed the overall project architecture (Manager, Builder/Strategy pattern), built the UI/terminal rendering engine with smart animation, and authored the Origin Shift generation algorithm (including the mandatory "42" pattern).
- **Planning & Evolution:** We started by building the core grid data structure and splitting the logic. The UI rendering was challenging due to terminal flickering, which we solved by implementing a targeted cell-redraw system. Adding multiple algorithms was a planned bonus feature. Packaging the project into `mazegen` was done in the final phase.
- **What worked well:** Dividing the architecture into visual (Renderer), logical (Builders/Solver), and configuration classes made the code highly modular, allowing both team members to work on algorithms and UI independently.
- **Tools used:** Git for version control, Makefile for automation, Poetry for package management, and Python's `venv`.

## Resources
- **AI Usage:** Generative AI (LLMs) was used as a pair-programming tool to:
  1. Optimize terminal rendering logic (ANSI escape codes) to prevent screen flickering.
  2. Understand and implement the 16-bit hexadecimal bitwise operations required for the `OUTPUT_FILE` format.
  3. Refactor the `pyproject.toml` to properly package our source code into the `mazegen` wheel format.
  All AI-generated snippets were thoroughly reviewed, tested, and modified to fit our architecture.
- **References:** Wikipedia (Maze generation algorithms), official Python documentation for `setuptools` and `typing`.