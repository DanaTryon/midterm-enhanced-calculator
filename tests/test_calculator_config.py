import os
import pytest
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_config_initialization():
    config = CalculatorConfig()
    assert isinstance(config.base_dir, Path)
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value > Decimal("1e10")
    assert config.default_encoding == "utf-8"


def test_custom_config_values(tmp_path):
    config = CalculatorConfig(
        base_dir=tmp_path,
        max_history_size=50,
        auto_save=False,
        precision=5,
        max_input_value=Decimal("100"),
        default_encoding="ascii"
    )
    assert config.base_dir == tmp_path
    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 5
    assert config.max_input_value == Decimal("100")
    assert config.default_encoding == "ascii"


def test_config_paths(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    assert config.log_dir == tmp_path / "logs"
    assert config.history_dir == tmp_path / "history"
    assert config.log_file == tmp_path / "logs" / "calculator.log"
    assert config.history_file == tmp_path / "history" / "calculator_history.csv"


def test_config_validation_success():
    config = CalculatorConfig(
        max_history_size=10,
        precision=2,
        max_input_value=Decimal("100")
    )
    config.validate()  # Should not raise


def test_validate_max_history_size_failure():
    config = CalculatorConfig(max_history_size=0)
    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        config.validate()


def test_validate_precision_failure():
    config = CalculatorConfig(precision=0)
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        config.validate()


def test_validate_max_input_value_failure():
    config = CalculatorConfig(max_input_value=Decimal("-1"))
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        config.validate()
