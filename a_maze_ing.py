from argparse import ArgumentParser, Namespace, ArgumentTypeError
from srcs.maze_config.maze import Maze
from srcs.maze_config.parse_config import load_config
import os
import sys

def main() -> None:

    parser: ArgumentParser = ArgumentParser(
        description=(
        "This program implements a maze generator that takes a configuration file, "
        "generates a maze, "
        "and writes it to a file using a hexadecimal wall representation. "
        "It also provides a visual representation of the maze."
        ),
        usage="venv/bin/python %(prog)s [<path>]"
    )

    parser.add_argument(
        "config_file",
        type=check_file_exists,
        help="Path to the configuration file"
    )

    args: Namespace = parser.parse_args()

    try:
        parsed_config = load_config(args.config_file)
        maze = Maze(parsed_config)
        print(maze)

    except Exception as e:
        print(f"[Error]: {e}", file=sys.stderr)
        sys.exit(1)



def check_file_exists(path: str) -> str:
    """
    Validates whether the given path exists, points to a regular file,
    is not a hidden file, and has a valid '.txt' extension.

    :param path: Path to the configuration file
    :type path: str
    :return: Validated file path
    :rtype: str
    :raises ArgumentTypeError: If the file is invalid
    """

    # Existence check
    if not os.path.exists(path):
        raise ArgumentTypeError(f"File not found: {path}")

    # Must be a real file, not a directory
    if not os.path.isfile(path):
        raise ArgumentTypeError(f"The provided path is not a file: {path}")

    filename: str = os.path.basename(path)

    # Hidden file check
    if filename.startswith("."):
        raise ArgumentTypeError("Hidden files are not allowed as config files")

    # Extension check
    if not filename.lower().endswith(".txt"):
        raise ArgumentTypeError(f"Config file must be a .txt file: {path}")

    return (path)


if __name__ == "__main__":
    main()