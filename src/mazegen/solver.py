"""
Breadth-First Search (BFS) shortest path solver for the maze.
"""

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Tuple

from .grid import Grid

Coord = Tuple[int, int]


@dataclass(frozen=True)
class SolveResult:
    """Encapsulates the result of a pathfinding operation.

    Attributes:
        path_coords (List[Coord]): A list of (x, y) tuples representing
            the sequence of cells from start to goal.
        path_dirs (str): A string of directions (e.g., "NNESW")
            corresponding to the steps taken.
    """
    path_coords: List[Coord]
    path_dirs: str


class Solver:
    """Shortest-path solver using the Breadth-First Search algorithm.

    This class navigates the grid's cells, checking open paths to find
    the optimal guaranteed shortest route between two points.

    Attributes:
        grid (Grid): The maze grid object to be solved.
    """

    _DIRS: Dict[str, Coord] = {
        "north": (0, -1),
        "east": (1, 0),
        "south": (0, 1),
        "west": (-1, 0),
    }

    _DIR_LETTER: Dict[str, str] = {
        "north": "N",
        "east": "E",
        "south": "S",
        "west": "W",
    }

    _OPPOSITE: Dict[str, str] = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }

    def __init__(self, grid: Grid) -> None:
        """Initializes the Solver.

        Args:
            grid (Grid): The grid structure to run the solver on.
        """
        self.grid: Grid = grid

    def solve(self, start: Coord, goal: Coord) -> SolveResult:
        """Solves the maze from the start coordinate to the goal.

        Args:
            start (Coord): The (x, y) tuple of the starting point.
            goal (Coord): The (x, y) tuple of the exit point.

        Returns:
            SolveResult: An object containing the path coordinates and
            direction string. Returns empty values if no path is found.
        """
        if not self._in_bounds(start) or not self._in_bounds(goal):
            return SolveResult([], "")

        sx, sy = start
        gx, gy = goal

        if (self.grid.matrix[sy][sx].forbidden or
                self.grid.matrix[gy][gx].forbidden):
            return SolveResult([], "")

        q: Deque[Coord] = deque([start])
        visited: Set[Coord] = {start}
        prev: Dict[Coord, Optional[Coord]] = {start: None}
        prev_dir: Dict[Coord, Optional[str]] = {start: None}

        while q:
            cur: Coord = q.popleft()

            if cur == goal:
                return self._reconstruct(prev, prev_dir, goal)

            for direction, nxt in self._neighbors(cur):
                if nxt in visited:
                    continue
                visited.add(nxt)
                prev[nxt] = cur
                prev_dir[nxt] = direction
                q.append(nxt)

        return SolveResult([], "")

    def _neighbors(self, coord: Coord) -> List[Tuple[str, Coord]]:
        """Finds all reachable, non-forbidden neighboring cells.

        Checks paths (walls) between the current cell and adjacent ones
        to ensure a valid passage exists.

        Args:
            coord (Coord): The (x, y) tuple of the current cell.

        Returns:
            List[Tuple[str, Coord]]: A list of valid neighbors, each containing
            the direction taken and the neighbor's coordinate.
        """
        x, y = coord
        cell = self.grid.matrix[y][x]

        if cell.forbidden:
            return []

        out: List[Tuple[str, Coord]] = []
        for direction, (dx, dy) in self._DIRS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.grid.grid_width and
                    0 <= ny < self.grid.grid_height):
                continue

            ncell = self.grid.matrix[ny][nx]
            if ncell.forbidden:
                continue

            # Ensure there is a path leaving the current cell
            if not cell.paths.get(direction, False):
                continue

            # Ensure the neighbor is also open from its side
            opp: str = self._OPPOSITE[direction]
            if not ncell.paths.get(opp, False):
                continue

            out.append((direction, (nx, ny)))

        return out

    def _reconstruct(
        self,
        prev: Dict[Coord, Optional[Coord]],
        prev_dir: Dict[Coord, Optional[str]],
        goal: Coord,
    ) -> SolveResult:
        """Backtracks from the goal to the start to build the path sequence.

        Args:
            prev (Dict[Coord, Optional[Coord]]):
                Mapping of cells to their parents.
            prev_dir (Dict[Coord, Optional[str]]):
                Mapping of cells to the direction taken to reach them.
            goal (Coord): The target coordinate to backtrack from.

        Returns:
            SolveResult: The finalized path coordinates and direction string.
        """
        coords: List[Coord] = []
        letters: List[str] = []

        cur: Optional[Coord] = goal
        while cur is not None:
            coords.append(cur)
            d: Optional[str] = prev_dir.get(cur)
            if d is not None:
                letters.append(self._DIR_LETTER[d])
            cur = prev.get(cur)

        coords.reverse()
        letters.reverse()
        return SolveResult(coords, "".join(letters))

    def _in_bounds(self, coord: Coord) -> bool:
        """Checks if a coordinate falls within the grid's dimensions.

        Args:
            coord (Coord): The (x, y) tuple to check.

        Returns:
            bool: True if the coordinate is inside the grid, False otherwise.
        """
        x, y = coord
        return 0 <= x < self.grid.grid_width and 0 <= y < self.grid.grid_height
