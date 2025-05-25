"""Model generator and related functions."""

from pathlib import Path
from typing import Self

from reflex_generate.parser import ModelParser


class ModelGenerator:
    """TODO: Docstring this."""

    def __init__(self, parser: ModelParser, app_root: Path) -> Self:
        """
        Initializes the ModelGenerator with a ModelParser and an app root path.

        Args:
            parser (ModelParser): A ModelParser instance containing the model definition to generate.
            app_root (str): The root directory path of the application.

        Returns:
            Self
        """
        self._parser = parser
        self._model_folder = app_root / "models"

    def generate(self):
        """
        Generates the model class code from the provided definitions and stores it at `self._file_name`.

        Args:
            None

        Returns:
            None
        """
        lines = [f"class {self._parser.model_name}(rx.Model, table=True):"]
        for k, v in self._parser.fields.items():
            lines.append(f"    {k}: {v}")
        model = "\n".join(lines)
        model += "\n"

        self._model_folder.mkdir(parents=True, exist_ok=True)
        file_path = self._model_folder / f"{self._parser.model_name.lower()}.py"

        with file_path.open("w", encoding="utf-8") as f:
            f.write(model)
