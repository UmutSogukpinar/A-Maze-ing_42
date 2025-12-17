from __future__ import annotations

class Cell:
    x : int
    y : int

    visited : bool
    blocked : bool

    west : bool
    east : bool
    north : bool
    south : bool

    # ==== solve state (A*) ====

    g = float("inf")
    h = 0
    f = float("inf")
    parent : Cell | None = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.visited = False
        self.blocked = False

        self.north = True
        self.south = True
        self.east  = True
        self.west  = True


    def __lt__(self, other: Cell) -> bool:
        """
        Less-than comparison for A* priority queue.

        :param other: The other cell to compare with
        :type other: Cell
        :return: True if this cell has a lower f value than the other
        :rtype: bool
        """

        if self.f != other.f:
            return self.f < other.f
        
        return (self.y, self.x) < (other.y, other.x)

    
    def encode_walls(self) -> str:
        """
        Encode the walls of the cell into a 4-bit integer.

        Bit 0 (1): North wall
        Bit 1 (2): East wall
        Bit 2 (4): South wall
        Bit 3 (8): West wall

        Returns:
            str: Hexadecimal representation of the wall configuration.
        """

        code : int = 0
        hex_digits : str = "0123456789ABCDEF"

        if self.north:
            code |= 1
        if self.east:
            code |= 2
        if self.south:
            code |= 4
        if self.west:
            code |= 8

        return (hex_digits[code])
