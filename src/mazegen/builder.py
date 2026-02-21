import random
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from .grid import Grid
from .cell import Cell


class BaseBuilder(ABC):
    """Abstract base class for all maze generation algorithms.

    Ensures that each generator implements the necessary interface
    for step-by-step execution and terminal animation.

    Attributes:
        name (str): Algorithm name for display in the UI and Registry.
        grid (Grid): The grid object on which the maze will be built.
        deltas (Dict[str, Tuple[int, int]]): Mapping of cardinal directions
            to (dx, dy) coordinate changes.
        opposites (Dict[str, str]): Mapping of cardinal directions
            to their opposites.
    """
    name: str = "base_builder"

    def __init__(self, grid: Grid) -> None:
        """Initializes the base builder with a grid and direction maps.

        Args:
            grid (Grid): The grid object to operate on.
        """
        self.grid: Grid = grid
        self.deltas: Dict[str, Tuple[int, int]] = {
            "north": (0, -1),
            "south": (0, 1),
            "east": (1, 0),
            "west": (-1, 0)
        }
        self.opposites: Dict[str, str] = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }

    @abstractmethod
    def setup(self) -> None:
        """Prepares the grid for generation.

        This method should clean passages, reset visited flags,
        and set the starting point for the algorithm.
        Must be implemented in every derived class.
        """
        ...

    @abstractmethod
    def step(self) -> List[Cell]:
        """Executes one iteration of the algorithm.

        Used by the Manager to animate the generation process step-by-step.

        Returns:
            List[Cell]: A list of cells that have visually changed
            during this step and need to be redrawn.
        """
        ...


class DFSBuilder(BaseBuilder):
    """Maze generator based on Depth-First Search (Recursive Backtracker).

    Creates a maze by carving a random path and backtracking when reaching
    a dead end. Adapted for step-by-step execution to provide smooth
    terminal animation. Supports 'braid' (imperfect) maze generation
    by occasionally carving loops.

    Attributes:
        stack (List[Tuple[int, int]]): A stack of (x, y) coordinates tracking
            the current path. Used for backtracking from dead ends.
    """

    name: str = "dfs_backtracker"

    def __init__(self, grid: Grid) -> None:
        """Initializes the DFS generator.

        Args:
            grid (Grid): The grid object on which the maze will be built.
        """
        super().__init__(grid)
        self.stack: List[Tuple[int, int]] = []

    def setup(self) -> None:
        """Prepares the grid for DFS generation.

        Clears all passages, resets visited flags and vectors.
        Finds the starting cell using the 'is_start' flag and pushes it
        onto the stack to begin generation.
        """
        start_cell: Cell | None = None

        for row in self.grid.matrix:
            for cell in row:
                if not cell.forbidden:
                    cell.visited = False
                    cell.vector = None
                    cell.is_solution = False
                    for k in cell.paths:
                        cell.paths[k] = False

                if cell.is_start:
                    start_cell = cell

        if start_cell:
            start_cell.visited = True
            self.stack = [(start_cell.cell_x, start_cell.cell_y)]

    def step(self) -> List[Cell]:
        """Performs a single iteration of the DFS algorithm.

        Finds unvisited neighbors. If none exist, backtracks (or creates
        a loop if perfection is disabled). Otherwise, carves a path to a
        random unvisited neighbor.

        Returns:
            List[Cell]: A list of cells that have visually changed
            during this step.
        """
        if not self.stack:
            return []

        x, y = self.stack[-1]
        current_cell = self.grid.matrix[y][x]

        neighbors: List[Tuple[int, int, str]] = []
        for direction, (dx, dy) in self.deltas.items():
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.grid.grid_width and
                    0 <= ny < self.grid.grid_height):
                ncell = self.grid.matrix[ny][nx]
                if not ncell.forbidden and not ncell.visited:
                    neighbors.append((nx, ny, direction))

        if not neighbors:
            updates: List[Cell] = [current_cell]

            if hasattr(self.grid, 'perfection') and not self.grid.perfection:
                if random.random() < 0.10:
                    visited_neighbors: List[Tuple[Cell, str]] = []
                    for d, (dx, dy) in self.deltas.items():
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.grid.grid_width and
                                0 <= ny < self.grid.grid_height):
                            ncell = self.grid.matrix[ny][nx]
                            if (ncell.visited and not ncell.forbidden
                                    and not current_cell.paths[d]):
                                visited_neighbors.append((ncell, d))

                    if visited_neighbors:
                        target_cell, direction = (
                            random.choice(visited_neighbors))
                        current_cell.paths[direction] = True
                        target_cell.paths[self.opposites[direction]] = True

                        updates.append(target_cell)

            self.stack.pop()
            if self.stack:
                px, py = self.stack[-1]
                updates.append(self.grid.matrix[py][px])

            return updates

        nx, ny, direction = random.choice(neighbors)
        next_cell: Cell = self.grid.matrix[ny][nx]

        current_cell.paths[direction] = True
        next_cell.paths[self.opposites[direction]] = True
        next_cell.visited = True

        self.stack.append((nx, ny))

        return [current_cell, next_cell]


class OriginShift(BaseBuilder):
    """Maze generator based on the Origin Shift concept.

    A variation of Aldous-Broder and Wilson's algorithms that guarantees
    a uniform spanning tree. This specific implementation includes
    a predefined vector field to carve a '42' Easter egg in the center.

    Attributes:
        origin (Cell | None): The current 'empty' cell or sink towards
            which all other flow vectors point.
    """
    name: str = "origin_shift"

    def __init__(self, grid: Grid) -> None:
        """Initializes the Origin Shift generator.

        Args:
            grid (Grid): The grid object on which the maze will be built.
        """
        super().__init__(grid)
        self.origin: Cell | None = None

    def setup(self) -> None:
        """Prepares the grid and sets up initial flow vectors.

        Clears existing passages and configures a default flow vector for
        each cell, overriding specific coordinates to create the '42' shape.
        """
        w: int = self.grid.grid_width
        h: int = self.grid.grid_height

        for row in self.grid.matrix:
            for cell in row:
                cell.paths = {k: False for k in cell.paths}
                cell.vector = None
                cell.is_solution = False

        # Center coordinates for the '42' Easter egg
        sx: int = (w - 7) // 2
        sy: int = (h - 5) // 2

        overrides: dict[tuple[int, int], str] = {
            (1, 0): "north", (1, 1): "north",
            (3, 0): "south", (3, 1): "south",
            (3, 2): "south", (3, 3): "south", (3, 4): "south",
            (4, 1): "west", (5, 1): "west",
            (0, 3): "south", (1, 3): "south", (0, 4): "south", (1, 4): "south",
            (5, 3): "south", (6, 3): "south"
        }

        for y in range(h):
            for x in range(w):
                cell = self.grid.matrix[y][x]

                if cell.forbidden:
                    continue

                if x == w - 1 and y == h - 1:
                    self.origin = cell
                    cell.vector = None
                    continue

                direction: str | None = None
                rel_pos: tuple[int, int] = (x - sx, y - sy)

                if rel_pos in overrides:
                    desired: str = overrides[rel_pos]
                    if self._is_valid_move(x, y, desired):
                        direction = desired

                if not direction:
                    if self._is_valid_move(x, y, "east"):
                        direction = "east"
                    elif self._is_valid_move(x, y, "south"):
                        direction = "south"
                    elif self._is_valid_move(x, y, "north"):
                        direction = "north"
                    elif self._is_valid_move(x, y, "west"):
                        direction = "west"

                if direction:
                    self._set_vector(cell, direction)
                else:
                    self.origin = cell
                    cell.vector = None

    def _set_vector(self, cell: Cell, direction: str) -> None:
        """Sets the flow vector for a cell and opens the corresponding wall."""
        cell.vector = direction
        cell.paths[direction] = True
        dx, dy = self.deltas[direction]
        neighbor: Cell = self.grid.matrix[cell.cell_y + dy][cell.cell_x + dx]
        neighbor.paths[self.opposites[direction]] = True

    def _is_valid_move(self, x: int, y: int, direction: str) -> bool:
        """Checks if a move is within bounds and not on a forbidden cell."""
        dx, dy = self.deltas[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.grid.grid_width and
                0 <= ny < self.grid.grid_height):
            return False
        if self.grid.matrix[ny][nx].forbidden:
            return False
        return True

    def _close_wall(self, cell: Cell, direction: str) -> None:
        """Closes the passage between a cell and its neighbor."""
        cell.paths[direction] = False
        dx, dy = self.deltas[direction]
        neighbor: Cell = self.grid.matrix[cell.cell_y + dy][cell.cell_x + dx]
        neighbor.paths[self.opposites[direction]] = False

    def _get_valid_neighbors(self, cell: Cell) -> list[tuple[Cell, str]]:
        """Returns a list of valid neighboring cells and their directions."""
        candidates: list[tuple[Cell, str]] = []
        for direction, (dx, dy) in self.deltas.items():
            nx, ny = cell.cell_x + dx, cell.cell_y + dy
            if (0 <= nx < self.grid.grid_width and
                    0 <= ny < self.grid.grid_height):
                neighbor: Cell = self.grid.matrix[ny][nx]
                if not neighbor.forbidden:
                    candidates.append((neighbor, direction))
        return candidates

    def step(self) -> List[Cell]:
        """Performs one iteration of the Origin Shift algorithm.

        Randomly selects a valid neighbor, shifts the origin to it,
        and updates vectors and walls accordingly. Optionally carves loops
        if perfection is disabled.

        Returns:
            List[Cell]: A list of cells that have changed visually.
        """
        updates: List[Cell] = []

        current_origin: Cell | None = self.origin
        if not current_origin:
            return []

        neighbors: list[tuple[Cell, str]] = (
            self._get_valid_neighbors(current_origin))
        if not neighbors:
            return []

        target, direction = random.choice(neighbors)

        current_origin.visited = True
        target.visited = True

        if target.vector:
            should_close: bool = True

            if hasattr(self.grid, 'perfection') and not self.grid.perfection:
                if random.random() < 0.05:
                    should_close = False

            if should_close:
                dx, dy = self.deltas[target.vector]
                old_neighbor: Cell = (
                    self.grid.matrix)[target.cell_y + dy][target.cell_x + dx]
                self._close_wall(target, target.vector)
                updates.append(old_neighbor)

        self._set_vector(current_origin, direction)
        target.vector = None
        self.origin = target

        updates.append(current_origin)
        updates.append(target)

        return updates


class PrimBuilder(BaseBuilder):
    """Maze generator based on Randomized Prim's algorithm.

    Creates a highly branching maze with many short dead ends. It maintains
    a 'frontier' of cells adjacent to the current maze and randomly selects
    one to connect to the maze at each step.

    Attributes:
        frontier (List[Tuple[int, int, int, int, str]]): A list of potential
            next cells to process. Each tuple contains:
            (cell_x, cell_y, parent_x, parent_y, direction_from_parent).
    """

    name: str = "prim"

    def __init__(self, grid: Grid) -> None:
        """Initializes the Prim's algorithm generator.

        Args:
            grid (Grid): The grid object on which the maze will be built.
        """
        super().__init__(grid)
        self.frontier: List[Tuple[int, int, int, int, str]] = []

    def setup(self) -> None:
        """Prepares the grid for Prim's generation.

        Resets all cell states, identifies the starting cell, and initializes
        the frontier list with the neighbors of the starting cell.
        """
        start_cell: Cell | None = None

        for row in self.grid.matrix:
            for cell in row:
                if cell.forbidden:
                    continue

                cell.visited = False
                cell.vector = None
                cell.is_solution = False
                for k in cell.paths:
                    cell.paths[k] = False

                if cell.is_start:
                    start_cell = cell

        # Fallback if no start cell is designated
        if not start_cell:
            for row in self.grid.matrix:
                for cell in row:
                    if not cell.forbidden:
                        start_cell = cell
                        break
                if start_cell:
                    break

        self.frontier = []
        if start_cell:
            start_cell.visited = True
            self._add_frontier(start_cell.cell_x, start_cell.cell_y)

    def step(self) -> List[Cell]:
        """Performs one iteration of Prim's algorithm.

        Pops a random cell from the frontier, connects it to its parent,
        and adds its valid neighbors to the frontier. Occasionally carves
        loops if the maze is not set to perfect.

        Returns:
            List[Cell]: A list of cells that have visually changed.
        """
        while self.frontier:
            idx: int = random.randrange(len(self.frontier))
            x, y, px, py, d = self.frontier.pop(idx)

            cell: Cell = self.grid.matrix[y][x]
            parent: Cell = self.grid.matrix[py][px]

            if cell.forbidden or cell.visited:
                continue
            if parent.forbidden or not parent.visited:
                continue

            updates: List[Cell] = []

            parent.paths[d] = True
            cell.paths[self.opposites[d]] = True
            cell.visited = True

            updates.append(parent)
            updates.append(cell)

            self._add_frontier(x, y)

            if hasattr(self.grid, "perfection") and not self.grid.perfection:
                if random.random() < 0.08:
                    loop_target: Tuple[Cell, str] | None = (
                        self._pick_visited_neighbor_without_passage(cell))
                    if loop_target:
                        target_cell, direction = loop_target
                        cell.paths[direction] = True
                        target_cell.paths[self.opposites[direction]] = True
                        updates.append(target_cell)

            return updates

        return []

    def _add_frontier(self, x: int, y: int) -> None:
        """Identifies valid, unvisited neighbors and adds them to the frontier.

        Args:
            x (int): The x-coordinate of the current cell.
            y (int): The y-coordinate of the current cell.
        """
        for d, (dx, dy) in self.deltas.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.grid.grid_width and
                    0 <= ny < self.grid.grid_height):
                continue

            ncell: Cell = self.grid.matrix[ny][nx]
            if ncell.forbidden or ncell.visited:
                continue

            self.frontier.append((nx, ny, x, y, d))

    def _pick_visited_neighbor_without_passage(self, cell: Cell)\
            -> Tuple[Cell, str] | None:
        """Selects a random visited neighbor to carve a loop.

        Args:
            cell (Cell): The cell from which to look for neighbors.

        Returns:
            Tuple[Cell, str] | None: A tuple containing the target neighbor
            and the direction to it, or None if no such neighbor exists.
        """
        candidates: List[Tuple[Cell, str]] = []
        x, y = cell.cell_x, cell.cell_y

        for d, (dx, dy) in self.deltas.items():
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.grid.grid_width and
                    0 <= ny < self.grid.grid_height):
                ncell: Cell = self.grid.matrix[ny][nx]
                if ncell.forbidden:
                    continue
                if ncell.visited and not cell.paths[d]:
                    candidates.append((ncell, d))

        if not candidates:
            return None

        return random.choice(candidates)


class KruskalBuilder(BaseBuilder):
    """Maze generator based on Randomized Kruskal's algorithm.

    Uses a Union-Find (Disjoint Set) data structure to build a minimum
    spanning tree, ensuring a perfect maze. Adapted for step-by-step
    execution to allow terminal animation.

    Attributes:
        parent (Dict[Tuple[int, int], Tuple[int, int]]): Tracks the parent
            of each cell for the Union-Find data structure.
        rank (Dict[Tuple[int, int], int]): Tracks the rank of each tree
            to optimize the union operation.
        edges (List[Tuple[Tuple[int, int], Tuple[int, int], str]]): A
            shuffled list of all possible walls (edges) between adjacent
            valid cells.
    """

    name: str = "kruskal"

    # Directions to check to avoid duplicating edges (only east and south)
    _EDGES_DIRS: Tuple[Tuple[str, Tuple[int, int]], ...] = (
        ("east", (1, 0)),
        ("south", (0, 1)),
    )

    def __init__(self, grid: Grid) -> None:
        """Initializes the Kruskal generator.

        Args:
            grid (Grid): The grid object on which the maze will be built.
        """
        super().__init__(grid)
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.rank: Dict[Tuple[int, int], int] = {}
        self.edges: List[Tuple[Tuple[int, int], Tuple[int, int], str]] = []

    def setup(self) -> None:
        """Prepares the grid and initializes Union-Find structures.

        Resets all cells, assigns each valid cell to its own disjoint set,
        and builds a randomized list of all internal edges (walls) that
        could potentially be carved.
        """
        for row in self.grid.matrix:
            for cell in row:
                if cell.forbidden:
                    continue
                cell.visited = False
                cell.is_solution = False
                cell.vector = None
                for k in cell.paths:
                    cell.paths[k] = False

        self.parent = {}
        self.rank = {}
        self.edges = []

        for y in range(self.grid.grid_height):
            for x in range(self.grid.grid_width):
                if self.grid.matrix[y][x].forbidden:
                    continue
                c: Tuple[int, int] = (x, y)
                self.parent[c] = c
                self.rank[c] = 0

        for y in range(self.grid.grid_height):
            for x in range(self.grid.grid_width):
                if self.grid.matrix[y][x].forbidden:
                    continue
                for d, (dx, dy) in self._EDGES_DIRS:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.grid.grid_width and
                            0 <= ny < self.grid.grid_height):
                        if self.grid.matrix[ny][nx].forbidden:
                            continue
                        self.edges.append(((x, y), (nx, ny), d))

        random.shuffle(self.edges)

    def step(self) -> List[Cell]:
        """Processes a single edge from the randomized list.

        Pops an edge and checks if the connected cells belong to different
        sets. If they do, unions the sets and carves a passage. Occasionally
        carves loops if perfection is disabled.

        Returns:
            List[Cell]: A list of cells that have visually changed.
        """
        while self.edges:
            a: Tuple[int, int]
            b: Tuple[int, int]
            d: str

            a, b, d = self.edges.pop()
            ra: Tuple[int, int] = self._find(a)
            rb: Tuple[int, int] = self._find(b)

            if ra == rb:
                if (hasattr(self.grid, "perfection") and
                        not self.grid.perfection):
                    if random.random() < 0.06:
                        return self._carve_and_mark(a, b, d)
                continue

            self._union(ra, rb)
            return self._carve_and_mark(a, b, d)

        return []

    def _find(self, x: Tuple[int, int]) -> Tuple[int, int]:
        """Finds the root of the set containing x with path compression.

        Args:
            x (Tuple[int, int]): The coordinate to find the root for.

        Returns:
            Tuple[int, int]: The root coordinate of the set.
        """
        if self.parent[x] != x:
            self.parent[x] = self._find(self.parent[x])
        return self.parent[x]

    def _union(self, a: Tuple[int, int], b: Tuple[int, int]) -> None:
        """Unions two sets by rank.

        Args:
            a (Tuple[int, int]): Root of the first set.
            b (Tuple[int, int]): Root of the second set.
        """
        if self.rank[a] < self.rank[b]:
            self.parent[a] = b
        elif self.rank[a] > self.rank[b]:
            self.parent[b] = a
        else:
            self.parent[b] = a
            self.rank[a] += 1

    def _carve_and_mark(self, a: Tuple[int, int],
                        b: Tuple[int, int],
                        d: str) -> List[Cell]:
        """Carves a passage between two adjacent cells.

        Args:
            a (Tuple[int, int]): First cell coordinates.
            b (Tuple[int, int]): Second cell coordinates.
            d (str): Direction from cell 'a' to cell 'b'.

        Returns:
            List[Cell]: The updated cells to be redrawn.
        """
        ax, ay = a
        bx, by = b
        cell: Cell = self.grid.matrix[ay][ax]
        ncell: Cell = self.grid.matrix[by][bx]

        cell.paths[d] = True
        ncell.paths[self.opposites[d]] = True

        cell.visited = True
        ncell.visited = True

        return [cell, ncell]
