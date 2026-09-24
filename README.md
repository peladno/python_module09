# Python Module 09: Data Validation & Modeling with Pydantic

Welcome to **Python Module 09** of the 42 Tokyo Python curriculum. This module introduces data validation, schema enforcement, and type safety using Pydantic through space-themed exercises.

## 🎯 Objectives

- Define robust data models using Pydantic `BaseModel` and `Field`.
- Apply and enforce field constraints (length limits, numerical ranges, optional types, and default values).
- Utilize custom `Enum` classes for strict categorical data.
- Implement contextual cross-field business logic using `@model_validator(mode='after')`.
- Validate complex nested data structures and model lists (`list[Model]`).
- Ensure static typing compliance under `mypy --strict`.

---

## 📁 Directory Structure & Exercises

| Exercise | Directory | File(s)            | Description                                                                  |
| :------- | :-------- | :----------------- | :--------------------------------------------------------------------------- |
| **ex0**  | `ex0/`    | `space_station.py` | Space station data validation with `BaseModel` and `Field` constraints.      |
| **ex1**  | `ex1/`    | `alien_contact.py` | Alien contact log validation using `Enum` and custom cross-field validators. |
| **ex2**  | `ex2/`    | `space_crew.py`    | Space mission and crew management with nested models and team requirements.  |

---

## 🚀 How to Run

### 1. Setup Environment

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Execute Exercises

To execute any exercise, navigate into this directory (or run directly with Python):

```bash
python ex0/space_station.py
python ex1/alien_contact.py
python ex2/space_crew.py
```

### 3. Type Checking

Run strict type checking with mypy across all exercises:

```bash
mypy --strict .
```
