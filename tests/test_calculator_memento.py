import datetime
from decimal import Decimal
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_to_dict_and_from_dict():
    # Create a sample calculation
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    history = [calc]

    # Create memento
    memento = CalculatorMemento(history=history)
    memento_dict = memento.to_dict()

    # Validate dictionary structure
    assert "history" in memento_dict
    assert "timestamp" in memento_dict
    assert isinstance(memento_dict["history"], list)
    assert isinstance(memento_dict["timestamp"], str)

    # Recreate memento from dict
    restored = CalculatorMemento.from_dict(memento_dict)
    assert isinstance(restored, CalculatorMemento)
    assert len(restored.history) == 1
    assert restored.history[0] == calc
    assert isinstance(restored.timestamp, datetime.datetime)
