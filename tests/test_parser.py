"""Tests for parser.py."""

import pytest

from reflex_generate.parser import ModelParser


def test_valid_model_parsing():
    """Test that valid model definitions are parsed correctly."""
    model_name = "User"
    fields = ("name:string", "age:int", "is_active:bool")
    parser = ModelParser(model_name, fields)

    assert parser.model_name == "User"
    assert parser.fields == {"name": "string", "age": "int", "is_active": "bool"}


def test_invalid_type_raises_error():
    """Test that invalid types raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        ModelParser("User", ("name:invalidtype",))

    assert "Invalid type" in str(excinfo.value)


def test_malformed_field_raises_error():
    """Test that malformed field definitions raise errors."""
    with pytest.raises(ValueError):
        ModelParser("User", ("name_without_type",))

    with pytest.raises(ValueError):
        ModelParser("User", ("name:type:extra",))


def test_all_allowed_types_work():
    """Test that all allowed types are accepted."""
    fields = tuple(f"field_{t}:{t}" for t in ModelParser.ALLOWED_TYPES)
    parser = ModelParser("TestModel", fields)

    assert len(parser.fields) == len(ModelParser.ALLOWED_TYPES)
    for t in ModelParser.ALLOWED_TYPES:
        assert f"field_{t}" in parser.fields
        assert parser.fields[f"field_{t}"] == t
