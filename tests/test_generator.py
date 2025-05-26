"""Tests for generator.py."""

from pathlib import Path

import pytest

from reflex_generate.generator import ModelGenerator
from reflex_generate.parser import ModelParser


@pytest.fixture
def sample_parser():
    """Fixture providing a sample ModelParser instance."""
    return ModelParser("User", ("name:str", "age:int"))


@pytest.fixture
def temp_app_root(tmp_path):
    """Fixture providing a temporary app root directory."""
    return tmp_path / "test_app"


def test_generator_initialization(sample_parser, temp_app_root):
    """Test that generator initializes correctly."""
    generator = ModelGenerator(sample_parser, temp_app_root)

    assert generator._parser == sample_parser
    assert generator._model_folder == temp_app_root / "models"


def test_generate_creates_directory(sample_parser, temp_app_root):
    """Test that generate() creates the models directory if needed."""
    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    assert (temp_app_root / "models").exists()
    assert (temp_app_root / "models").is_dir()


def test_generate_creates_model_file(sample_parser, temp_app_root):
    """Test that generate() creates the correct model file."""
    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    expected_file = temp_app_root / "models" / "user.py"
    assert expected_file.exists()
    assert expected_file.is_file()


def test_generate_writes_correct_content(sample_parser, temp_app_root):
    """Test that generate() writes the correct content to the file."""
    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    expected_content = (
        "class User(rx.Model, table=True):\n" + "    name: str\n" + "    age: int\n"
    )
    actual_content = Path(temp_app_root / "models" / "user.py").read_text()
    assert expected_content == actual_content


def test_generate_handles_existing_dir(sample_parser, temp_app_root):
    """Test that generate() works when models directory exists."""
    (temp_app_root / "models").mkdir(parents=True)
    generator = ModelGenerator(sample_parser, temp_app_root)

    # Should not raise an exception
    generator.generate()
