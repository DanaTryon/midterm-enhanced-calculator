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

### `.env` File

Create a `.env` file in the project root to configure environment variables:

```env
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These variables control:

- CALCULATOR_MAX_HISTORY_SIZE: Limits the number of stored history entries (default: 100)

- CALCULATOR_AUTO_SAVE: Enables automatic saving of history after each operation

- CALCULATOR_DEFAULT_ENCODING: Sets the encoding used for reading/writing history files

Make sure your application loads these values using load_dotenv().

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






