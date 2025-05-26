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
        self._app_root = app_root
        self._app_name = app_root.name
        self._model_folder = app_root / "models"

    def generate(self):
        """
        Generates the model class code from the provided definitions, imports it at `models/__init__.py`,
        and imports it within the application.

        Args:
            None

        Returns:
            None
        """
        # Creating the model class file
        lines = [
            f"import reflex as rx\n\nclass {self._parser.model_name}(rx.Model, table=True):"
        ]
        for k, v in self._parser.fields.items():
            lines.append(f"    {k}: {v}")
        model = "\n".join(lines)
        model += "\n"

        self._model_folder.mkdir(parents=True, exist_ok=True)
        file_path = (
            self._model_folder / f"{self._parser.model_name.lower()}.py"
        )

        with file_path.open("w", encoding="utf-8") as f:
            f.write(model)

        # Importing the model at `models/__init__.py`
        init_module_path = self._model_folder / "__init__.py"
        if init_module_path.exists():
            prev_init_text = init_module_path.read_text()
            with init_module_path.open("w", encoding="utf-8") as f:
                new_init_text = (
                    f"from .{self._parser.model_name.lower()} "
                    f"import {self._parser.model_name}\n"
                )
                joined_text = new_init_text + prev_init_text
                f.write(joined_text)
        else:
            with init_module_path.open("w", encoding="utf-8") as f:
                f.write(
                    f"from .{self._parser.model_name.lower()} "
                    f"import {self._parser.model_name}\n"
                )

        # Importing the model at `rxconfig.py` (this is temporary, should be where the index view is stored)
        import_statement_rxconfig = (
            f"from {self._app_name}.models "
            f"import {self._parser.model_name.lower()}\n\n"
        )

        rxconfig_path = Path(self._app_root / "rxconfig.py")
        rxconfig_text = rxconfig_path.read_text()

        merged_imports = import_statement_rxconfig + rxconfig_text

        with rxconfig_path.open("w", encoding="utf-8") as f:
            f.write(merged_imports)
