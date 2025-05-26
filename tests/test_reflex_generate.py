"""Tests for reflex_generate.py (CLI)."""

from unittest.mock import patch

from click.testing import CliRunner

from reflex_generate.reflex_generate import cli


@patch("reflex_generate.reflex_generate.check_dependencies")
def test_cli_checks_dependencies(mock_check_deps):
    """Test that the CLI checks dependencies."""
    runner = CliRunner()
    runner.invoke(cli, ["model", "User", "name:str"])
    mock_check_deps.assert_called_once()


@patch("reflex_generate.reflex_generate.ModelParser")
@patch("reflex_generate.reflex_generate.ModelGenerator")
@patch("reflex_generate.reflex_generate.get_app_root")
@patch("reflex_generate.reflex_generate.check_dependencies")
def test_model_command(
    mock_check_deps,
    mock_get_app_root,
    mock_model_generator,
    mock_model_parser,
):
    """Test the model command with valid arguments."""
    mock_parser_instance = mock_model_parser.return_value
    mock_generator_instance = mock_model_generator.return_value
    mock_get_app_root.return_value = "/fake/app/root"

    runner = CliRunner()
    result = runner.invoke(cli, ["model", "User", "name:str", "age:int"])

    assert result.exit_code == 0
    mock_check_deps.assert_called_once()
    mock_model_parser.assert_called_with("User", ("name:str", "age:int"))
    mock_model_generator.assert_called_with(mock_parser_instance, "/fake/app/root")
    mock_generator_instance.generate.assert_called_once()


def test_scaffold_command():
    """Test the scaffold command (placeholder for now)."""
    runner = CliRunner()
    result = runner.invoke(cli, ["scaffold", "User", "name:str"])
    assert result.exit_code == 0
