from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Maze:
    width: int
    height: int
    entry: Point
    perfect: bool
    output_file: str

    DEFAULT_POS : int = 1

    def __init__(self, config_dict: dict[str, str]) -> None:

        try:
            allowed_keys : set[str] = {"width", "height", "entry", "perfect", "output_file"}

            for key in config_dict.keys():
                if key not in allowed_keys:
                    raise ValueError(f"Invalid variable in config file: '{key}'")
                
            self.width = int(config_dict.get("width", self.DEFAULT_POS))
            self.height = int(config_dict.get("height", self.DEFAULT_POS))
            self.perfect = config_dict.get("perfect", "false").lower() == "true"
            self.output_file = config_dict.get("output_file", "maze.txt")

            if "entry" in config_dict:
                self.entry = self.__parse_point(config_dict["entry"])
            else:
                self.entry = Point(0, 0)

        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
        
    def __repr__(self) -> str:
        return (
            f"Maze(width={self.width}, "
            f"height={self.height}, "
            f"entry={self.entry}, "
            f"perfect={self.perfect}, "
            f"output_file='{self.output_file}')"
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