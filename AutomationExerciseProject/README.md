# Playwright Python Automation Testing Framework

A beginner-friendly, maintainable, and production-ready test automation framework for the **[Automation Exercise](https://automationexercise.com/)** website built using **Python**, **Playwright**, **Pytest**, **Page Object Model (POM)**, and **Data-Driven Testing (CSV)**.

---

## 🛠️ Key Framework Features

- **Page Object Model (POM)**: Locators are maintained exclusively inside Page Object classes under `pages/`. Business flows remain in test files under `tests/`.
- **Zero Hardcoded Product Data**: Test Case 1 dynamically inspects available categories, subcategories, and products from the website at runtime.
- **Reproducible Randomization**: Accepts or generates a random seed (`TEST_SEED`) to reproduce exact test runs when needed.
- **Data-Driven Testing**: Test Case 2 reads login credentials dynamically from `test_data/login_data.csv` using Pytest parameterization. Adding rows automatically expands test execution.
- **No `time.sleep()`**: Uses Playwright auto-waiting, web assertions (`expect`), and `domcontentloaded` page load strategies.
- **Structured Fixtures & Logging**: Reusable fixtures in `conftest.py` with detailed console logging.

---

## 📁 Project Structure

```text
AutomationExerciseProject/
│
├── pages/                          # Page Object Model classes
│   ├── __init__.py
│   ├── home_page.py                # Homepage navigation & login state checks
│   ├── products_page.py            # Category navigation & product listings
│   ├── product_detail_page.py      # Product details & add to cart functionality
│   ├── cart_page.py                # Cart contents & line item assertions
│   └── login_page.py               # Login form & error validation
│
├── tests/                          # Automated business test suites
│   ├── __init__.py
│   ├── test_guest_cart_persistence.py  # Test Case 1: Dynamic Guest Cart Persistence
│   └── test_login_data_driven.py       # Test Case 2: Data-Driven Login using CSV
│
├── test_data/                      # External test data files
│   └── login_data.csv              # CSV file containing login accounts
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   └── csv_reader.py               # Reusable CSV file parser
│
├── conftest.py                     # Pytest fixtures (Browser, Context, Page, POMs)
├── pytest.ini                      # Pytest runner configuration & logging setup
├── requirements.txt                # Python package dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+** installed.
- Pip package manager.

### 1. Install Dependencies

Install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

Install the Playwright Chromium browser binary:

```bash
playwright install chromium
```

---

## 🧪 Running Tests

### Run All Tests

To run the complete test suite with detailed output:

```bash
pytest
```

---

### Run Test Case 1 — Guest Cart Persistence After Login

Verifies that products selected dynamically as a guest remain preserved in the cart after user login.

```bash
pytest tests/test_guest_cart_persistence.py -s -v
```

#### Reproducing a Test Run with a Specific Seed

Test Case 1 logs a **Random Seed** during execution. To rerun a scenario with a specific seed:

**On Windows PowerShell:**
```powershell
$env:TEST_SEED="784521"; pytest tests/test_guest_cart_persistence.py -s -v
```

**On Windows CMD:**
```cmd
set TEST_SEED=784521 && pytest tests/test_guest_cart_persistence.py -s -v
```

---

### Run Test Case 2 — Data-Driven Login Using CSV

Executes login validation dynamically for every account listed in `test_data/login_data.csv`.

```bash
pytest tests/test_login_data_driven.py -s -v
```

---

## ➕ Adding More Login Accounts

You can test additional accounts without modifying any Python code.

Simply add new rows to `test_data/login_data.csv`:

```csv
email,password,expected_result
auto_test_1789484613@example.com,TestPassword123,success
auto_test_1789484613@example.com,WrongPass123,failure
invalid_user_99999@example.com,Password123,failure
new_user@example.com,secret123,success
```

Pytest will automatically detect the new rows and run parameterized test instances for each account!

---

## 📋 Technology Stack

- **[Playwright Python](https://playwright.dev/python/)**: Fast, reliable browser automation.
- **[Pytest](https://docs.pytest.org/)**: Robust test runner & assertion framework.
- **Page Object Model (POM)**: Maintainable object-oriented UI architecture.
- **Data-Driven Testing (CSV)**: Decoupled test data & test logic.
