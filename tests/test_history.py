import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver


def test_logging_observer_valid(monkeypatch):
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))

    # Patch logging.info to capture the log message
    messages = []
    monkeypatch.setattr("logging.info", lambda msg: messages.append(msg))

    observer = LoggingObserver()
    observer.update(calc)

    assert any("Calculation performed: Addition (2, 3) = 5" in msg for msg in messages)


def test_logging_observer_none_input():
    observer = LoggingObserver()
    with pytest.raises(AttributeError, match="Calculation cannot be None"):
        observer.update(None)


def test_autosave_observer_valid(monkeypatch):
    class DummyConfig:
        auto_save = True

    class DummyCalculator:
        config = DummyConfig()
        saved = False

        def save_history(self):
            self.saved = True

    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    dummy = DummyCalculator()

    # Patch logging.info to suppress actual logging
    monkeypatch.setattr("logging.info", lambda msg: None)

    observer = AutoSaveObserver(dummy)
    observer.update(calc)

    assert dummy.saved is True


def test_autosave_observer_none_input():
    class DummyConfig:
        auto_save = True

    class DummyCalculator:
        config = DummyConfig()
        def save_history(self): pass

    observer = AutoSaveObserver(DummyCalculator())
    with pytest.raises(AttributeError, match="Calculation cannot be None"):
        observer.update(None)


def test_autosave_observer_invalid_calculator():
    class BadCalculator:
        pass

    with pytest.raises(TypeError, match="Calculator must have 'config' and 'save_history' attributes"):
        AutoSaveObserver(BadCalculator())
