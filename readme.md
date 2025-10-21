# 🧮 Enhanced Calculator CLI

A modular, test-driven command-line calculator built for academic and professional use. This application supports a wide range of arithmetic operations, undo/redo functionality, persistent history, and color-coded output for improved user experience.

---

## 📦 Project Description

This calculator is designed using clean architecture principles and incorporates multiple design patterns including Factory and Memento. It supports:

- Arithmetic operations: `add`, `subtract`, `multiply`, `divide`, `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff`
- History tracking with undo/redo
- Persistent save/load functionality using CSV
- Input validation and exception handling
- Color-coded output using `colorama`
- 100% test coverage with `pytest`
- CI/CD integration via GitHub Actions


---

## 📁 Project Structure

```
midterm-enhanced-calculator/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── operations.py
│   └── logger.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_operations.py
│   └── ...
├── .env
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── tests.yml
```
---

## 🛠️ Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/DanaTryon/midterm-enhanced-calculator.git
cd midterm-enhanced-calculator
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration Setup
This application uses a `.env` file and the `python-dotenv` package to manage configuration settings. All environment variables are loaded at startup and validated to ensure safe defaults.

#### ✅ Create a .env File in the Project Root

```bash
# Base Directories
CALCULATOR_BASE_DIR=./
CALCULATOR_LOG_DIR=./logs
CALCULATOR_HISTORY_DIR=./history
CALCULATOR_LOG_FILE=./logs/calculator.log
CALCULATOR_HISTORY_FILE=./history/calculator_history.csv

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=3
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

#### ✅ What Each Variable Does

| Variable	       |   Purpose                   |
|------------------|-----------------------------|
|CALCULATOR_BASE_DIR	|  Root directory for calculator data|
|CALCULATOR_LOG_DIR	|Directory where log files are stored|
|CALCULATOR_HISTORY_DIR	|Directory where history files are stored|
|CALCULATOR_LOG_FILE	|Full path to the log file|
|CALCULATOR_HISTORY_FILE	|Full path to the history CSV file|
|CALCULATOR_MAX_HISTORY_SIZE	|Maximum number of entries stored in history|
|CALCULATOR_AUTO_SAVE	|Automatically save history after each operation (true or false)|
|CALCULATOR_PRECISION	|Number of decimal places for calculation results|
|CALCULATOR_MAX_INPUT_VALUE	|Maximum allowed input value for calculations|
|CALCULATOR_DEFAULT_ENCODING	|Encoding used for file operations (utf-8, ascii, etc.)|



#### ✅ How It Works
- The .env file is loaded using python-dotenv

- All values are accessed via os.getenv() inside calculator_config.py

- Defaults are applied if values are missing

- Validation is performed at startup to catch misconfigurations

---

## 🧑‍💻 Usage Guide

Run the calculator:

```bash
python main.py
```

### Supported Commands

| Command       | Description                              |
|---------------|------------------------------------------|
| `add`         | Add two numbers                          |
| `subtract`    | Subtract second number from first        |
| `multiply`    | Multiply two numbers                     |
| `divide`      | Divide first number by second            |
| `power`       | Raise first number to the power of second|
| `root`        | Take the nth root of a number            |
| `modulus`     | Return remainder of division             |
| `int_divide`  | Integer division                         |
| `percent`     | Calculate first number percentage of second |
| `abs_diff`    | Absolute difference of two numbers       |
| `history`     | Show calculation history                 |
| `clear`       | Clear history                            |
| `undo`        | Undo last calculation                    |
| `redo`        | Redo last undone calculation             |
| `save`        | Save history to file                     |
| `load`        | Load history from file                   |
| `exit`        | Exit the calculator                      |

### Color-Coded Output

- ✅ Results: Green  
- ❌ Errors: Red  
- ℹ️ Prompts: Cyan  

---

## 🧪 Testing Instructions

Run all tests with coverage:

```bash
pytest --cov=app --cov-fail-under=70
```

- ✅ 100% test coverage across all modules
- ✅ 112 unit tests passing
- ✅ Coverage report saved to `htmlcov/`

---

## 🔁 CI/CD Information

This project uses GitHub Actions for continuous integration:

- Runs on every push and pull request
- Installs dependencies and runs tests
- Enforces minimum coverage threshold
- Flags any failing tests or coverage drops

Workflow file: `.github/workflows/python-app.yml`

---

## 🧼 Code Documentation

All modules and classes include:

- ✅ Docstrings describing purpose and usage
- ✅ Inline comments for clarity
- ✅ Logical separation of concerns

Example:

```python
class Multiplication(Operation):
    """
    Multiplication operation implementation.

    Performs the multiplication of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Multiply two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Product of the two operands.
        """
        self.validate_operands(a, b)
        return a * b
```

---

## 📝 Logging Setup

Logging is configured via the `.env` file and initialized in `calculator.py`:

```python
 # Configure the basic logging settings
            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  # Overwrite any existing logging configuration
            )
```

Logs include operation flow, errors, and history actions.






