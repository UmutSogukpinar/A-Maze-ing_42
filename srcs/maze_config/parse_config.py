def load_config(path: str) -> dict[str, str]:
    """
    Loads and parses a configuration file into a dictionary.

    The configuration file must follow the 'key=value' format.
    Empty lines and full-line comments starting with '#' are ignored.
    Inline comments on the right side of values are also supported.

    :param path: Path to the configuration file
    :type path: str
    :return: Parsed configuration as a key-value dictionary
    :rtype: dict[str, str]
    """
    
    config: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            # Remove leading/trailing whitespaces and newline
            line = line.strip()

            # Skip empty lines and full-line comments
            if not line or line.startswith("#"):
                continue

            # Ensure key-value separator exists
            if "=" not in line:
                raise ValueError(f"Line {line_no}: missing '=' -> {line}")

            # Split only on the first '='
            key, value = line.split("=", 1)

            # Remove inline comments from value
            value = value.split("#", 1)[0].strip().lower()
            key = key.strip().lower()

            # Reject empty key or empty value
            if not key or not value:
                raise ValueError(f"Line {line_no}: invalid key/value -> {line}")

            config[key] = value

    return (config)
