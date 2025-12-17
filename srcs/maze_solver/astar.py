from typing import Set
from srcs.maze_generator.cell import Cell

import heapq

def solve_astar(
    grid: list[list[Cell]],
    start: Cell,
    goal: Cell
) -> list[Cell]:
    
    """
    Solve the maze using the A* algorithm.
    
    :param grid: The grid of cells representing the maze
    :type grid: list[list[Cell]]
    :param start: The starting cell
    :type start: Cell
    :param goal: The goal cell
    :type goal: Cell
    :return: The path from start to goal as a list of cells
    :rtype: list[Cell]
    """

    open_heap: list[tuple[int, Cell]] = []
    already_check_set: Set[Cell] = set()

    start.g = 0
    start.h = heuristic(start, goal)
    start.f = start.g + start.h
    start.parent = None

    heapq.heappush(open_heap, (start.f, start))

    while open_heap:

        current : Cell
        p : int

        # No need for the priority value here
        p, current = heapq.heappop(open_heap)

        if current == goal:
            return (reconstruct_path(goal))

        already_check_set.add(current)

        for neighbor in neighbors(current, grid):

            if neighbor.blocked:
                continue

            if neighbor in already_check_set:
                continue

            tentative_g : int = current.g + 1

            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                heapq.heappush(open_heap, neighbor)

    return ([])



def neighbors(cell: Cell, grid: list[list[Cell]]) -> list[Cell]:
    result: list[Cell] = []
    """
    Find all neighbors of a cell in the grid.

    :param cell: The cell to find neighbors for
    :type cell: Cell
    :param grid: The grid of cells
    :type grid: list[list[Cell]]
    :return: A list of neighboring cells
    :rtype: list[Cell]
    """

    x = cell.x
    y = cell.y

    if not cell.north:
        result.append(grid[y - 1][x])
    if not cell.south:
        result.append(grid[y + 1][x])
    if not cell.west:
        result.append(grid[y][x - 1])
    if not cell.east:
        result.append(grid[y][x + 1])

    return (result)


def heuristic(a: Cell, b: Cell) -> int:
    """
    Calculate the Manhattan distance between two cells.

    :param a: Base cell
    :type a: Cell
    :param b: Target cell
    :type b: Cell
    :return: Manhattan distance between the two cells
    :rtype: int
    """

    return (abs(a.x - b.x) + abs(a.y - b.y))


def reconstruct_path(end: Cell) -> list[Cell]:
    """
    Reconstruct the path from start to end by following parent pointers.

    :param end: The end cell
    :type end: Cell
    :return: The reconstructed path as a list of cells
    :rtype: list[Cell]
    """
    path: list[Cell] = []
    cur: Cell | None = end

    while cur is not None:
        path.append(cur)
        cur = cur.parent

    path.reverse()
    return (path)

def path_to_dir(path: list[Cell]) -> list[str]:
    """
    Convert a path of cells into a list of directions.

    :param path: The path as a list of cells
    :type path: list[Cell]
    :return: The path as a list of directions
    :rtype: list[str]
    """

    if not path or len(path) < 2:
        return ([])

    directions: list[str] = []

    for i in range(1, len(path)):
        prev = path[i - 1]
        curr = path[i]

        if curr.x == prev.x:
            if curr.y == prev.y - 1:
                directions.append("N")
            elif curr.y == prev.y + 1:
                directions.append("S")
        elif curr.y == prev.y:
            if curr.x == prev.x - 1:
                directions.append("W")
            elif curr.x == prev.x + 1:
                directions.append("E")

    return (directions)