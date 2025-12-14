from typing import List
from srcs.maze_config.maze import Maze
from srcs.maze_generator.cell import Cell

class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.grid: list[list[Cell]] = self.__init_grid()
        self.__apply_42_mask()

    def __init_grid(self) -> list[list[Cell]]:
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

    
    def debug_print_grid(self) -> None:
        """
        Print the logical maze grid for debugging purposes.

        The grid is printed row by row and represents the internal
        logical state of each cell.

        Legend:
            B : Blocked cell (42 pattern)
            . : Unvisited cell
            V : Visited cell

        :param self: The MazeGenerator instance.
        :type self: MazeGenerator
        :return: None
        :rtype: None
        """

        for y in range(self.maze.height):
            row = []
            for x in range(self.maze.width):
                cell = self.grid[y][x]

                if cell.blocked:
                    row.append("B")
                elif cell.visited:
                    row.append("V")
                else:
                    row.append(".")

            print(" ".join(row))

