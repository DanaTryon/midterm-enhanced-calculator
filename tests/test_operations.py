import pytest
from decimal import Decimal
from app.operations import (
    Addition, Subtraction, Multiplication, Division,
    Power, Root, OperationFactory
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

