from argparse import ArgumentParser, Namespace, ArgumentTypeError
import os


def check_file_exists(path: str) -> str:
    """
    Validates if the provided path exists, is a file,
    is not a hidden file, and has a valid .txt extension.
    """

    filename: str = os.path.basename(path)

    # Hidden file check
    if filename.startswith("."):
        raise ArgumentTypeError("Hidden files are not allowed as config files")

    # Extension check
    if not filename.lower().endswith(".txt"):
        raise ArgumentTypeError(f"Config file must be a .txt file: {path}")

    # Existence check
    if not os.path.exists(path):
        raise ArgumentTypeError(f"File not found: {path}")
    
    # Must be a real file, not a directory
    if not os.path.isfile(path):
        raise ArgumentTypeError(f"The provided path is not a file: {path}")
    
    return (path)



def main() -> None:

    parser: ArgumentParser = ArgumentParser(
        description=(
        "This program implements a maze generator that takes a configuration file, "
        "generates a maze, "
        "and writes it to a file using a hexadecimal wall representation. "
        "It also provides a visual representation of the maze."
        ),
        usage="venv/bin/python %(prog)s [--config_file <path>]"
    )

    parser.add_argument(
        "--config_file",
        type=check_file_exists,
        required=True,
        help="Path to the configuration file"
    )

    args: Namespace = parser.parse_args()

    print(f"Config file path: {args.config_file}")

if __name__ == "__main__":
    main()