"""Tests for generator.py."""

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
    app_root = tmp_path / "test_app"
    app_root.mkdir()
    # Create empty rxconfig.py
    (app_root / "rxconfig.py").write_text("")
    return app_root


def test_generator_initialization(sample_parser, temp_app_root):
    """Test that generator initializes correctly."""
    generator = ModelGenerator(sample_parser, temp_app_root)

    assert generator._parser == sample_parser
    assert generator._app_root == temp_app_root
    assert generator._app_name == "test_app"
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
        "import reflex as rx\n\n"
        + "class User(rx.Model, table=True):\n"
        + "    name: str\n"
        + "    age: int\n"
    )
    actual_content = (temp_app_root / "models" / "user.py").read_text()
    assert expected_content == actual_content


def test_generate_handles_existing_dir(sample_parser, temp_app_root):
    """Test that generate() works when models directory exists."""
    (temp_app_root / "models").mkdir(parents=True)
    generator = ModelGenerator(sample_parser, temp_app_root)

    # Should not raise an exception
    generator.generate()


def test_generate_creates_init_file(sample_parser, temp_app_root):
    """Test that generate() creates __init__.py with correct content."""
    init_file = temp_app_root / "models" / "__init__.py"
    assert not init_file.exists()

    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    assert init_file.exists()

    expected_content = "from .user import User\n"
    assert init_file.read_text() == expected_content


def test_generate_updates_existing_init_file(sample_parser, temp_app_root):
    """Test that generate() updates existing __init__.py correctly."""
    models_dir = temp_app_root / "models"
    models_dir.mkdir()
    init_file = models_dir / "__init__.py"
    init_file.write_text("from .existing import ExistingModel\n")

    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    expected_content = (
        "from .user import User\nfrom .existing import ExistingModel\n"
    )
    assert init_file.read_text() == expected_content


def test_generate_updates_rxconfig_file(sample_parser, temp_app_root):
    """Test that generate() updates rxconfig.py with correct import."""
    rxconfig_path = temp_app_root / "rxconfig.py"
    original_content = "import reflex as rx\n\n"
    rxconfig_path.write_text(original_content)

    generator = ModelGenerator(sample_parser, temp_app_root)
    generator.generate()

    expected_content = (
        "from test_app.models import User\n\nimport reflex as rx\n\n"
    )
    assert rxconfig_path.read_text() == expected_content


def test_generate_with_complex_model(temp_app_root):
    """Test that generate() handles complex model definitions correctly."""
    complex_parser = ModelParser(
        "Product",
        ("name:str", "price:float", "in_stock:bool", "date:datetime"),
    )
    generator = ModelGenerator(complex_parser, temp_app_root)
    generator.generate()

    expected_content = (
        "import reflex as rx\n\n"
        + "class Product(rx.Model, table=True):\n"
        + "    name: str\n"
        + "    price: float\n"
        + "    in_stock: bool\n"
        + "    date: datetime\n"
    )
    actual_content = (temp_app_root / "models" / "product.py").read_text()
    assert expected_content == actual_content
