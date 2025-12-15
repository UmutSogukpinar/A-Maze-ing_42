from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Maze:
    width: int
    height: int
    entry: Point
    exit: Point
    perfect: bool
    output_file: str
    algorithm: str

    __DEFAULT_ENTRY_POS : str = "0,0"
    __DEFAULT_SIZE : int = 20
    __MIN_MAP_SIZE_X : int = 9
    __MIN_MAP_SIZE_Y : int = 7


    def __init__(self, config_dict: dict[str, str]) -> None:

        allowed_keys : set[str] = {"width", "height", "entry", "exit", "perfect", "output_file", "algorithm"}

        try:
            for key in config_dict.keys():
                if key not in allowed_keys:
                    raise ValueError(f"Invalid variable in config file: '{key}'")
            
            # Process the attributes
            self.width = int(config_dict.get("width", self.__DEFAULT_SIZE))
            self.height = int(config_dict.get("height", self.__DEFAULT_SIZE))
            self.perfect = config_dict.get("perfect", "false").lower() == "true"
            self.output_file = config_dict.get("output_file", "maze.txt")
            self.entry = self.__parse_point(config_dict.get("entry", self.__DEFAULT_ENTRY_POS))
            self.exit  = self.__parse_point(config_dict.get("exit", f"{self.width-1},{self.height-1}"))
            self.algorithm = config_dict.get("algorithm", "dfs").lower()

            # Check whether the attributes are valid or not
            self.__is_maze_valid()

        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
    
    
    def __repr__(self) -> str:
        return (
            f"Maze(width={self.width}, "
            f"height={self.height}, "
            f"entry={self.entry}, "
            f"exit={self.exit}, "
            f"perfect={self.perfect}, "
            f"output_file='{self.output_file}', "
            f"algorithm='{self.algorithm}')"
        )


    def __parse_point(self, raw: str) -> Point:
        """
        Parses a raw string in the format "x,y" into a Point object.

        The input string must contain exactly two integer coordinates
        separated by a comma. Both positive and negative integers are supported.

        :param raw: Raw coordinate string in the format "x,y"
        :type raw: str
        :return: Parsed Point object with integer coordinates
        :rtype: Point
        :raises ValueError: If the format is invalid or coordinates are not integers
        """

        parts = raw.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid point format: {raw}")

        x, y = parts
            
        if not (x.strip().lstrip('-').isdigit() and y.strip().lstrip('-').isdigit()):
            raise ValueError(f"Coordinates must be integers: {raw}")

        return (Point(int(x), int(y)))
    
    
    def __is_maze_valid(self) -> None:
        """
        Validates maze configuration constraints.

        This method ensures that:
        - Maze dimensions satisfy the minimum size requirements.
        - Entry and exit points are within maze bounds.
        - Entry and exit points are not the same.

        :param self: The Maze instance.
        :type self: Maze
        :return:
        :rtype: None
        :raises ValueError: If the maze size is smaller than the minimum
            allowed dimensions, if entry or exit points are out of bounds,
            or if entry and exit points are the same.
        """

        # Size validation (for 42 pattern)
        if self.width < self.__MIN_MAP_SIZE_X or self.height < self.__MIN_MAP_SIZE_Y:
            raise ValueError(
                f"Maze size too small. Minimum size is "
                f"{self.__MIN_MAP_SIZE_X}x{self.__MIN_MAP_SIZE_Y}."
            )

        # Entry / Exit bounds
        for name, point in (("entry", self.entry), ("exit", self.exit)):
            if point.x < 0 or point.y < 0:
                raise ValueError(f"{name.capitalize()} point out of bounds: {point}")

            if point.x >= self.width or point.y >= self.height:
                raise ValueError(f"{name.capitalize()} point out of bounds: {point}")

        # Entry and exit must differ
        if self.entry == self.exit:
            raise ValueError("Entry and exit points must be different.")

