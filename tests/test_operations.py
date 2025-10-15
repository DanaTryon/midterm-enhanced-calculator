import pytest
from decimal import Decimal
from app.operations import (
    Addition, Subtraction, Multiplication, Division,
    Power, Root, Modulus, IntegerDivision, Percentage, 
    AbsoluteDifference, OperationFactory
)
from app.exceptions import ValidationError


def test_addition():
    op = Addition()
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("5")


def test_subtraction():
    op = Subtraction()
    assert op.execute(Decimal("5"), Decimal("3")) == Decimal("2")


def test_multiplication():
    op = Multiplication()
    assert op.execute(Decimal("4"), Decimal("2.5")) == Decimal("10.0")


def test_division():
    op = Division()
    assert op.execute(Decimal("10"), Decimal("2")) == Decimal("5")


def test_division_by_zero():
    op = Division()
    with pytest.raises(ValidationError, match="Division by zero is not allowed"):
        op.execute(Decimal("10"), Decimal("0"))


def test_power():
    op = Power()
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("8.0")


def test_power_negative_exponent():
    op = Power()
    with pytest.raises(ValidationError, match="Negative exponents not supported"):
        op.execute(Decimal("2"), Decimal("-1"))


def test_root():
    op = Root()
    assert round(op.execute(Decimal("9"), Decimal("2")), 5) == Decimal("3.0")


def test_root_negative_number():
    op = Root()
    with pytest.raises(ValidationError, match="Cannot calculate root of negative number"):
        op.execute(Decimal("-9"), Decimal("2"))


def test_root_zero_degree():
    op = Root()
    with pytest.raises(ValidationError, match="Zero root is undefined"):
        op.execute(Decimal("9"), Decimal("0"))


def test_operation_factory_known():
    op = OperationFactory.create_operation("add")
    assert isinstance(op, Addition)


def test_operation_factory_unknown():
    with pytest.raises(ValueError, match="Unknown operation: unknown"):
        OperationFactory.create_operation("unknown")


def test_operation_factory_register():
    class DummyOp(Addition): pass
    OperationFactory.register_operation("dummy", DummyOp)
    op = OperationFactory.create_operation("dummy")
    assert isinstance(op, DummyOp)


def test_operation_factory_register_invalid():
    with pytest.raises(TypeError, match="Operation class must inherit from Operation"):
        OperationFactory.register_operation("bad", object)

def test_operation_str_methods():
    assert str(Addition()) == "Addition"
    assert str(Subtraction()) == "Subtraction"
    assert str(Multiplication()) == "Multiplication"
    assert str(Division()) == "Division"
    assert str(Power()) == "Power"
    assert str(Root()) == "Root"
    assert str(Modulus()) == "Modulus"
    assert str(IntegerDivision()) == "IntegerDivision"
    assert str(Percentage()) == "Percentage"

def test_modulus():
    op = Modulus()
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("1")

def test_modulus_by_zero():
    op = Modulus()
    with pytest.raises(ValidationError, match="Modulus by zero is not allowed"):
        op.execute(Decimal("10"), Decimal("0"))

def test_integer_division():
    op = IntegerDivision()
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("3")

def test_integer_division_by_zero():
    op = IntegerDivision()
    with pytest.raises(ValidationError, match="Integer division by zero is not allowed"):
        op.execute(Decimal("10"), Decimal("0"))

def test_percentage():
    op = Percentage()
    assert op.execute(Decimal("50"), Decimal("200")) == Decimal("25")

def test_percentage_of_zero():
    op = Percentage()
    with pytest.raises(ValidationError, match="Cannot calculate percentage of zero"):
        op.execute(Decimal("50"), Decimal("0"))

def test_absolute_difference_positive():
    op = AbsoluteDifference()
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("7")

def test_absolute_difference_negative():
    op = AbsoluteDifference()
    assert op.execute(Decimal("3"), Decimal("10")) == Decimal("7")

def test_absolute_difference_zero():
    op = AbsoluteDifference()
    assert op.execute(Decimal("5"), Decimal("5")) == Decimal("0")



