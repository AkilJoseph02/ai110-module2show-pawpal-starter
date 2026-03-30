# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Schedulingk
1. Checks for any time conflicts with tasks in cases where ones either involving the same pet or different pets happen around the same time. Leaves a warning.
2. Sorts the tasks by start time.
3. Can be filtered by pet name or by status.
4. Automates reoccuring tasks (daily, weekly, etc) once they're completed.

### Testing PawPal+
python -m pytest -r p
========================================= test session starts ==========================================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\aj200\Downloads\CodePath AI Course\ai110-module2show-pawpal-starter
collected 7 items                                                                                       

tests\test_pawpal.py .......                                                                      [100%]

======================================= short test summary info ======================================== 
PASSED tests/test_pawpal.py::TestTaskCompletion::test_mark_aborted_changes_status
PASSED tests/test_pawpal.py::TestTaskCompletion::test_mark_complete_changes_status
PASSED tests/test_pawpal.py::TestTaskCompletion::test_mark_in_progress_changes_status
PASSED tests/test_pawpal.py::TestTaskAddition::test_add_duplicate_task_returns_false
PASSED tests/test_pawpal.py::TestTaskAddition::test_add_task_increases_pet_task_count
PASSED tests/test_pawpal.py::TestTaskAddition::test_add_task_returns_true_on_success
PASSED tests/test_pawpal.py::TestTaskAddition::test_remove_task_decreases_pet_task_count
========================================== 7 passed in 0.19s =========================================== 

Confidence Level: 3