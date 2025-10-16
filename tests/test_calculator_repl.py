import pytest
import tempfile
from unittest.mock import patch
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.calculator import Calculator



def test_repl_help_and_exit(capsys):
    with patch("builtins.input", side_effect=["help", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Available commands" in output
    assert "Goodbye" in output


def test_repl_addition(capsys):
    with patch("builtins.input", side_effect=["add", "2", "3", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Result: 5" in output


def test_repl_invalid_command(capsys):
    with patch("builtins.input", side_effect=["foobar", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Unknown command: 'foobar'" in output


def test_repl_cancel_operation(capsys):
    with patch("builtins.input", side_effect=["add", "cancel", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Operation cancelled" in output


def test_repl_history_display(capsys):
    with patch("builtins.input", side_effect=["add", "1", "1", "history", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Addition(1, 1) = 2" in output


def test_repl_clear_history(capsys):
    with patch("builtins.input", side_effect=["add", "1", "1", "clear", "history", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "History cleared" in output
    assert "No calculations in history" in output


def test_repl_undo_redo(capsys):
    with patch("builtins.input", side_effect=["add", "2", "2", "undo", "redo", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Operation undone" in output
    assert "Operation redone" in output


def test_repl_percent_operation(capsys):
    with patch("builtins.input", side_effect=["percent", "15", "200", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Result: 7.5" in output


def test_repl_divide_by_zero(capsys):
    with patch("builtins.input", side_effect=["divide", "10", "0", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Error: Division by zero is not allowed" in output

def test_repl_history_save_failure(capsys):
    with patch("app.calculator.Calculator.save_history", side_effect=Exception("Disk full")):
        with patch("builtins.input", side_effect=["add", "2", "3", "exit"]):
            calculator_repl()
    output = capsys.readouterr().out
    assert "Warning: Could not save history: Disk full" in output

def test_repl_undo_command_success(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        config = CalculatorConfig(base_dir=tmpdir)
        calc = Calculator(config=config)
        with patch("app.calculator_repl.Calculator", return_value=calc):
            with patch("builtins.input", side_effect=["add", "2", "3", "undo", "exit"]):
                calculator_repl()
        output = capsys.readouterr().out
        assert "Operation undone" in output

def test_repl_undo_nothing_to_undo(capsys):
    with patch("builtins.input", side_effect=["undo", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Nothing to undo" in output

def test_repl_redo_nothing_to_redo(capsys):
    with patch("builtins.input", side_effect=["redo", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Nothing to redo" in output

def test_repl_save_success(capsys):
    with patch("builtins.input", side_effect=["save", "exit"]):
        with patch("app.calculator.Calculator.save_history", return_value=None):
            calculator_repl()
    output = capsys.readouterr().out
    assert "History saved successfully" in output

def test_repl_save_failure(capsys):
    with patch("builtins.input", side_effect=["save", "exit"]):
        with patch("app.calculator.Calculator.save_history", side_effect=Exception("Disk full")):
            calculator_repl()
    output = capsys.readouterr().out
    assert "Error saving history: Disk full" in output

def test_repl_load_success(capsys):
    with patch("builtins.input", side_effect=["load", "exit"]):
        with patch("app.calculator.Calculator.load_history", return_value=None):
            calculator_repl()
    output = capsys.readouterr().out
    assert "History loaded successfully" in output

def test_repl_load_failure(capsys):
    with patch("builtins.input", side_effect=["load", "exit"]):
        with patch("app.calculator.Calculator.load_history", side_effect=Exception("Corrupted file")):
            calculator_repl()
    output = capsys.readouterr().out
    assert "Error loading history: Corrupted file" in output

def test_repl_cancel_second_operand(capsys):
    with patch("builtins.input", side_effect=["add", "2", "cancel", "exit"]):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Operation cancelled" in output

def test_repl_unexpected_error_during_operation(capsys):
    with patch("builtins.input", side_effect=["add", "2", "3", "exit"]):
        with patch("app.calculator.Calculator.perform_operation", side_effect=Exception("Boom")):
            calculator_repl()
    output = capsys.readouterr().out
    assert "Unexpected error: Boom" in output

def test_repl_keyboard_interrupt(capsys):
    def input_gen():
        yield from [KeyboardInterrupt()]
        while True:
            yield "exit"

    with patch("builtins.input", side_effect=input_gen()):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Operation cancelled" in output

def test_repl_eof_error(capsys):
    def input_gen():
        yield from [EOFError()]
        while True:
            yield "exit"

    with patch("builtins.input", side_effect=input_gen()):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Input terminated. Exiting..." in output

def test_repl_generic_exception(capsys):
    def input_gen():
        yield from [Exception("Loop crash")]
        while True:
            yield "exit"

    with patch("builtins.input", side_effect=input_gen()):
        calculator_repl()
    output = capsys.readouterr().out
    assert "Error: Loop crash" in output

def test_repl_fatal_error_on_init(capsys):
    with patch("app.calculator_repl.Calculator", side_effect=Exception("Init fail")):
        try:
            calculator_repl()
        except Exception:
            pass
    output = capsys.readouterr().out
    assert "Fatal error: Init fail" in output









