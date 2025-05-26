"""Attribute parser and related functions."""

from typing import Self


class ModelParser:
    """
    Parses and validates model field definitions provided in 'name:type' format.

    This class processes a model name and a tuple of field strings, ensuring
    that each field has a valid type. The resulting field data can be used
    for generating model representations such as classes, schemas, or files.

    Attributes:
        model_name (str): The name of the model being parsed.
        fields (dict[str, str]): A dictionary mapping field names to their validated types.
    """

    ALLOWED_TYPES = {"int", "float", "str", "bool", "date", "datetime"}

    def __init__(self, model_name: str, fields: tuple[str, ...]) -> Self:
        """
        Initializes the ModelParser with a model name and its fields.

        Args:
            model_name (str): The name of the model to create.
            fields (tuple[str, ...]): The fields of the model in 'name:type' format.

        Returns:
            Self
        """
        self._model_name = model_name
        self._fields = self._parse_fields(fields)

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

    @property
    def fields(self):
        """Returns the parsed and validated fields of the model."""
        return self._fields

    @property
    def model_name(self):
        """Returns the model name."""
        return self._model_name
