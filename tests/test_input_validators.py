import pytest
from decimal import Decimal
from app.input_validators import InputValidator
from app.exceptions import ValidationError


class DummyConfig:
    max_input_value = Decimal("1000")


def test_validate_number_int():
    result = InputValidator.validate_number(42, DummyConfig())
    assert result == Decimal("42")


def test_validate_number_float():
    result = InputValidator.validate_number(3.14, DummyConfig())
    assert result == Decimal("3.14")


def test_validate_number_str():
    result = InputValidator.validate_number("  7.5  ", DummyConfig())
    assert result == Decimal("7.5")


def test_validate_number_exceeds_max():
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed"):
        InputValidator.validate_number("1001", DummyConfig())


def test_validate_number_invalid_format():
    with pytest.raises(ValidationError, match="Invalid number format"):
        InputValidator.validate_number("not_a_number", DummyConfig())
