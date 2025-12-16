class Cell:
    x : int
    y : int

    visited : bool
    blocked : bool

    west : bool
    east : bool
    north : bool
    south : bool


    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.visited = False
        self.blocked = False

        self.north = True
        self.south = True
        self.east  = True
        self.west  = True

    
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
        if self.south:
            code |= 2
        if self.west:
            code |= 4
        if self.east:
            code |= 8

        return (hex_digits[code])
