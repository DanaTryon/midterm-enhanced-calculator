import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError


def test_addition_calculation():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert calc.result == Decimal("5")
    assert "Addition(2, 3) = 5" in str(calc)


def test_subtraction_calculation():
    calc = Calculation("Subtraction", Decimal("5"), Decimal("2"))
    assert calc.result == Decimal("3")


def test_multiplication_calculation():
    calc = Calculation("Multiplication", Decimal("4"), Decimal("2.5"))
    assert calc.result == Decimal("10.0")


def test_division_calculation():
    calc = Calculation("Division", Decimal("10"), Decimal("2"))
    assert calc.result == Decimal("5")


def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation("Division", Decimal("10"), Decimal("0"))


def test_power_calculation():
    calc = Calculation("Power", Decimal("2"), Decimal("3"))
    assert calc.result == Decimal("8.0")


def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation("Power", Decimal("2"), Decimal("-1"))


def test_root_calculation():
    calc = Calculation("Root", Decimal("9"), Decimal("2"))
    assert round(calc.result, 5) == Decimal("3.0")


def test_root_of_negative():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation("Root", Decimal("-9"), Decimal("2"))


def test_root_zero_degree():
    with pytest.raises(OperationError, match="Zero root is undefined"):
        Calculation("Root", Decimal("9"), Decimal("0"))


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation: UnknownOp"):
        Calculation("UnknownOp", Decimal("1"), Decimal("1"))


def test_to_dict_and_from_dict():
    original = Calculation("Addition", Decimal("2"), Decimal("3"))
    data = original.to_dict()
    restored = Calculation.from_dict(data)
    assert restored == original
    assert isinstance(restored.timestamp, datetime)


def test_repr_and_eq():
    calc1 = Calculation("Addition", Decimal("2"), Decimal("3"))
    calc2 = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert repr(calc1).startswith("Calculation(operation='Addition'")
    assert calc1 == calc2


def test_format_result_precision():
    calc = Calculation("Division", Decimal("1"), Decimal("3"))
    formatted = calc.format_result(5)
    assert formatted.startswith("0.33333")

def test_calculation_pow_domain_error():
    # This causes a math domain error inside pow()
    with pytest.raises(OperationError, match="Calculation failed:"):
        Calculation("Power", Decimal("-9.0"), Decimal("0.5"))

def test_from_dict_missing_key():
    bad_data = {
        'operation': 'Addition',
        'operand1': '2',
        # 'operand2' is missing
        'result': '5',
        'timestamp': datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data:"):
        Calculation.from_dict(bad_data)

def test_from_dict_invalid_decimal():
    bad_data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': 'not_a_number',
        'result': '5',
        'timestamp': datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data:"):
        Calculation.from_dict(bad_data)

def test_from_dict_invalid_timestamp():
    bad_data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '5',
        'timestamp': 'not-a-valid-timestamp'
    }
    with pytest.raises(OperationError, match="Invalid calculation data:"):
        Calculation.from_dict(bad_data)

def test_calculation_equality_with_non_calculation():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert (calc == "not a calculation") is False

def test_integer_division():
    calc = Calculation("IntegerDivision", Decimal("10"), Decimal("3"))
    assert calc.result == Decimal("3")

def test_modulus():
    calc = Calculation("Modulus", Decimal("10"), Decimal("3"))
    assert calc.result == Decimal("1")

def test_absolute_difference():
    calc = Calculation("AbsoluteDifference", Decimal("10"), Decimal("3"))
    assert calc.result == Decimal("7")

def test_percent():
    calc = Calculation("Percent", Decimal("200"), Decimal("15"))
    assert calc.result == Decimal("30")




