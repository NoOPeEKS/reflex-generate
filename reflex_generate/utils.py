"""CLI utils."""

from pathlib import Path


class NotReflexError(Exception):
    """
    A custom exception that is raised when the `reflex-generate`
    command is not called from the root of a Reflex app.
    """

    pass


def check_dependencies():
    """Checks if reflex is installed as a dependency."""
    import sys
    from importlib.util import find_spec

    if not find_spec("reflex"):
        sys.stdout.write("You must have `reflex` installed before using this app\n")
        exit(1)


def get_app_root() -> Path:
    """
    Returns the root path of a Reflex application by looking whether there is
    an `rxconfig.py` or not.

    Args:
        None

    Returns:
        Path: The path to the root of the reflex app.

    Raises:
        NotReflexError: If it couldnt find a Reflex application.
    """
    if Path("rxconfig.py").exists():
        return Path.cwd()
    else:
        raise NotReflexError(
            "Reflex app root folder not found. Please re-run the command at the "
            "root of your Reflex project."
        )
