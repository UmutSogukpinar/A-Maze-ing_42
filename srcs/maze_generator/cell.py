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
