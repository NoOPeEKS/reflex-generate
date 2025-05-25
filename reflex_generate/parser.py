"""Attribute parser and related functions."""

from typing import Self


class ModelParser:
    """TODO: Docstring this."""

    ALLOWED_TYPES = {"int", "float", "string", "bool", "date", "datetime"}

    def __init__(self, model_name: str, fields: tuple[str, ...]) -> Self:
        """
        Initializes the ModelParser with a model name and its fields.

        Args:
            model_name (str): The name of the model to create.
            fields (tuple[str, ...]): The fields of the model in 'name:type' format.

        Returns:
            Self
        """
        self.model_name = model_name
        self.fields = self._parse_fields(fields)

    def _parse_fields(self, fields: tuple[str, ...]) -> dict[str, str]:
        """
        Parses the fields into a dictionary and validates data types.

        Args:
            fields (tuple[str, ...]): A tuple of 'name:type' field definitions.

        Returns:
            dict[str, str]: A dictionary mapping field names to their types.

        Raises:
            ValueError: If an invalid type is specified.
        """
        field_dict = {}
        for field in fields:
            name, _type = field.split(":")
            if _type not in self.ALLOWED_TYPES:
                raise ValueError(
                    f"Invalid type '{_type}' for field '{name}'. "
                    f"Allowed types are: {', '.join(self.ALLOWED_TYPES)}."
                )
            field_dict[name] = _type

        return field_dict
