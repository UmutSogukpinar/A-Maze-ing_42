import random

from typing import Dict, List, Set, Tuple

from srcs.maze_config.maze import Maze
from srcs.maze_generator.cell import Cell

class MazeGenerator:

    __DIRECTIONS : Dict[str, Tuple[int, int]] = {
        "north": (0, -1),
        "south": (0,  1),
        "east": (1,  0),
        "west": (-1, 0),
    }

    __OPPOSITE_DIRS: Dict[str, str] = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }


    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.grid: List[List[Cell]] = self.__init_grid()
        self.__generate()
        self.__apply_42_mask()

    def __init_grid(self) -> List[List[Cell]]:
        """
        Initialize the logical maze grid.

        This method creates a 2D grid of Cell objects based on the maze
        width and height.

        :param self: The MazeGenerator instance.
        :return: A 2D list representing the logical maze grid.
        :rtype: list[list[Cell]]
        """

        return [
            [Cell(x=x, y=y) for x in range(self.maze.width)]
            for y in range(self.maze.height)
        ]
    

    def __apply_42_mask(self) -> None:
        """
        Apply the '42' reserved area mask to the maze grid.

        This method marks a predefined pattern of cells in the center
        of the maze as blocked. Blocked cells are excluded from the
        maze generation algorithm and cannot be visited or connected
        by corridors.

        The pattern is centered within the maze grid and applied
        before running the maze generation algorithm.

        :param self: The MazeGenerator instance.
        :return: None
        :rtype: None
        """

        # 42 pattern
        pattern : List[str] = [
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        ]

        pattern_height : int = len(pattern)        # 5
        pattern_width : int = len(pattern[0])      # 7

        if self.maze.width < pattern_width or self.maze.height < pattern_height:
            raise ValueError("Maze is too small to place the 42 pattern.")
        
        offset_x : int = (self.maze.width  - pattern_width) // 2
        offset_y : int = (self.maze.height - pattern_height) // 2

        # Apply mask
        for y, row in enumerate(pattern):
            for x, ch in enumerate(row):
                if ch == "1":
                    self.grid[offset_y + y][offset_x + x].blocked = True

    
    def debug_print_cell_walls(self) -> None:
        """
        Visualize the maze using ASCII characters.

        Walls are represented by '#'
        Corridors are represented by spaces ' '
        """

        out_height = 2 * self.maze.height + 1
        out_width  = 2 * self.maze.width  + 1

        canvas: list[list[str]] = [
            ["#" for _ in range(out_width)]
            for _ in range(out_height)
        ]

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.grid[y][x]

                cy = 2 * y + 1
                cx = 2 * x + 1

                # Blocked cells stay closed
                if cell.blocked:
                    continue

                # Cell interior
                canvas[cy][cx] = " "

                # Open walls
                if not cell.north:
                    canvas[cy - 1][cx] = " "
                if not cell.south:
                    canvas[cy + 1][cx] = " "
                if not cell.west:
                    canvas[cy][cx - 1] = " "
                if not cell.east:
                    canvas[cy][cx + 1] = " "

        for row in canvas:
            print("".join(row))


    def __generate(self) -> None:

        ALGOS : set[str] = {"dfs"}

        if self.maze.algorithm not in ALGOS:
            raise ValueError(f"Unsupported algorithm: {self.maze.algorithm}")
        
        if self.maze.algorithm == "dfs":
            start_cell : Cell = self.grid[self.maze.entry.y][self.maze.entry.x]
            self.__dfs(start_cell)

    def __dfs(self, currentCell: Cell) -> None:
        """
        Perform depth-first search maze generation from the given cell.

        :param currentCell: Current cell for DFS
        :type cell: Cell
        :return:
        :rtype: None
        """

        currentCell.visited = True

        neighbors = self.__get_unvisited_neighbors(currentCell)
        random.shuffle(neighbors)

        for direction, neighbor in neighbors:
            if not neighbor.visited:
                self.__remove_wall(currentCell, neighbor, direction)
                self.__dfs(neighbor)


    def __get_unvisited_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        """
        Return all unvisited and non-blocked neighboring cells.

        :param cell: Current cell
        :type cell: Cell
        :return: List of (direction, neighbor cell) tuples
        :rtype: list[tuple[str, Cell]]
        """

        neighbors: list[tuple[str, Cell]] = []

        for direction, (dx, dy) in self.__DIRECTIONS.items():
            nx : int = cell.x + dx
            ny : int = cell.y + dy

            if nx < 0 or ny < 0:
                continue
            if nx >= self.maze.width or ny >= self.maze.height:
                continue

            neighbor : Cell = self.grid[ny][nx]

            if neighbor.blocked or neighbor.visited:
                continue

            neighbors.append((direction, neighbor))

        return (neighbors)


    def __remove_wall(self, a: Cell, b: Cell, direction: str) -> None:
        """
        Remove the wall between two adjacent cells.

        :param a: First cell
        :type a: Cell
        :param b: Second cell
        :type b: Cell
        :param direction: Direction from a to b
        :type direction: str
        :return:
        :rtype: None
        """

        setattr(a, direction, False)
        setattr(b, self.__OPPOSITE_DIRS[direction], False)

        