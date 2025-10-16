import pytest
from unittest.mock import patch, PropertyMock 
from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.operations import Addition
from app.calculation import Calculation
from app.history import HistoryObserver
import pandas as pd
from pathlib import Path
from app.calculator_memento import CalculatorMemento
from app.operations import OperationFactory
from app.exceptions import OperationError


class DummyObserver(HistoryObserver):
    def __init__(self):
        self.updated = False
        self.last_calc = None

    def update(self, calculation: Calculation) -> None:
        self.updated = True
        self.last_calc = calculation


def test_calculator_initialization(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    assert calc.config == config
    assert isinstance(calc.history, list)
    assert calc.undo_stack == []
    assert calc.redo_stack == []


def test_set_operation_and_perform(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    result = calc.perform_operation("2", "3")
    assert result == Decimal("5")
    assert len(calc.history) == 1


def test_perform_operation_without_strategy():
    calc = Calculator()
    with pytest.raises(OperationError, match="No operation set"):
        calc.perform_operation("2", "3")


def test_perform_operation_invalid_input():
    calc = Calculator()
    calc.set_operation(Addition())
    with pytest.raises(ValidationError):
        calc.perform_operation("abc", "3")


def test_observer_notification():
    calc = Calculator()
    observer = DummyObserver()
    calc.add_observer(observer)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    assert observer.updated is True
    assert isinstance(observer.last_calc, Calculation)


def test_remove_observer():
    calc = Calculator()
    observer = DummyObserver()
    calc.add_observer(observer)
    calc.remove_observer(observer)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    assert observer.updated is False

def test_undo_redo_behavior(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    calc.perform_operation("4", "5")

    assert len(calc.history) == 2

    # Undo last operation
    assert calc.undo() is True
    assert len(calc.history) == 1
    assert calc.history[0].operand1 == Decimal("2")

    # Redo it
    assert calc.redo() is True
    assert len(calc.history) == 2
    assert calc.history[1].operand1 == Decimal("4")


def test_undo_redo_empty_stack():
    calc = Calculator()
    assert calc.undo() is False
    assert calc.redo() is False


def test_clear_history():
    calc = Calculator()
    calc.set_operation(Addition())
    calc.perform_operation("1", "1")
    calc.clear_history()
    assert calc.history == []
    assert calc.undo_stack == []
    assert calc.redo_stack == []


def test_show_history_format(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    history_lines = calc.show_history()
    assert history_lines == ["Addition(2, 3) = 5"]


def test_get_history_dataframe(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    df = calc.get_history_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df.iloc[0]["result"] == "5"


def test_save_and_load_history(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    calc.perform_operation("2", "3")
    calc.save_history()

    # Create a new calculator and load history
    calc2 = Calculator(config=config)
    calc2.load_history()
    assert len(calc2.history) == 1
    assert calc2.history[0].result == Decimal("5")

# Logging setup failure
def test_setup_logging_failure():
    with patch("logging.basicConfig", side_effect=RuntimeError("Logging failed")):
        with pytest.raises(RuntimeError, match="Logging failed"):
            Calculator()


# Directory creation
def test_setup_directories(tmp_path):
    from app.calculator import CalculatorConfig, Calculator
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Confirm directories were created
    assert config.log_dir.exists()
    assert config.history_dir.exists()


# validation error and generic exception in perform_operation()
from app.calculator import Calculator
from app.operations import Addition
from app.exceptions import ValidationError

def test_perform_operation_validation_error():
    calc = Calculator()
    calc.set_operation(Addition())
    with pytest.raises(ValidationError):
        calc.perform_operation("not_a_number", "2")



def test_perform_operation_generic_exception(monkeypatch):
 
    class BrokenOperation(Addition):
        def execute(self, a, b):
            raise RuntimeError("Boom")

    calc = Calculator()
    calc.set_operation(BrokenOperation())

    with pytest.raises(OperationError, match="Operation failed: Boom"):
        calc.perform_operation("1", "2")

# save_history() with empty history
def test_save_history_creates_empty_csv(tmp_path):
    from app.calculator import CalculatorConfig, Calculator
    import pandas as pd

    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.save_history()

    df = pd.read_csv(config.history_file)
    assert df.empty
    assert list(df.columns) == ['operation', 'operand1', 'operand2', 'result', 'timestamp']


# load_history() with non-existent file
def test_load_history_empty_file(tmp_path):
    from app.calculator import CalculatorConfig, Calculator
    config = CalculatorConfig(base_dir=tmp_path)
    config.history_dir.mkdir(parents=True, exist_ok=True)
    config.history_file.write_text("operation,operand1,operand2,result,timestamp\n")  # headers only

    calc = Calculator(config=config)
    assert calc.history == []


from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

def test_load_history_no_file(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.load_history()
    assert calc.history == []


def test_load_history_when_file_missing(tmp_path):
    from app.calculator import CalculatorConfig, Calculator

    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.load_history()

    assert calc.history == []

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
import pandas as pd

def test_save_history_empty(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.save_history()
    df = pd.read_csv(config.history_file)
    assert df.empty

def test_history_trims_to_max_size():
    config = CalculatorConfig()
    config.max_history_size = 3
    calc = Calculator(config=config)

    calc.set_operation(OperationFactory.create_operation("add"))

    calc.perform_operation("1", "1")
    calc.perform_operation("2", "2")
    calc.perform_operation("3", "3")
    calc.perform_operation("4", "4")  # triggers pop(0)

    history = calc.show_history()
    assert len(history) == 3
    assert not any("Addition(1, 1)" in entry for entry in history)
    assert any("Addition(2, 2)" in entry for entry in history)

def test_save_history_raises_operation_error():
    calc = Calculator()
    calc.set_operation(OperationFactory.create_operation("add"))
    calc.perform_operation("1", "1")  # Ensure history is not empty

    with patch("pandas.DataFrame.to_csv", side_effect=IOError("Disk full")):
        with pytest.raises(OperationError) as exc_info:
            calc.save_history()

    assert "Failed to save history: Disk full" in str(exc_info.value)

#def test_load_history_raises_operation_error():
 #   calc = Calculator()
#
 #   with patch("pandas.read_csv", side_effect=IOError("File corrupted")):
  #      with pytest.raises(OperationError) as exc_info:
   #         calc.load_history()
#
 #   assert "Failed to load history: File corrupted" in str(exc_info.value)

def test_load_history_raises_operation_error(tmp_path):
    # Subclass CalculatorConfig to override history_dir
    class TestConfig(CalculatorConfig):
        @property
        def history_dir(self):
            return tmp_path

    config = TestConfig()
    corrupted_file = config.history_file
    corrupted_file.write_text("corrupted,data\nnot,valid")

    calc = Calculator(config=config)

    with patch("pandas.read_csv", side_effect=IOError("File corrupted")):
        with pytest.raises(OperationError) as exc_info:
            calc.load_history()

    assert "Failed to load history: File corrupted" in str(exc_info.value)