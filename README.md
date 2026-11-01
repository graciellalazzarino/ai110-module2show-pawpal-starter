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

## 🖥️ Sample Output

Output of `python main.py` (tasks are added out of order and sorted by the scheduler; the date is whichever day you run it):

```
Today's Schedule for Jordan (Sunday, November 01, 2026)
-------------------------------------------------------
  07:30  Luna   Breakfast        (10 min, high)     [ ]
  08:00  Mochi  Morning walk     (30 min, high)     [ ]
  14:00  Luna   Vet checkup      (60 min, high)     [ ]
  18:30  Mochi  Evening walk     (30 min, medium)   [ ]
```

## 🧪 Testing PawPal+

Run the full test suite from the project folder:

```bash
python -m pytest
```

`tests/test_pawpal.py` contains 14 tests covering:

- **Basics:** marking a task complete; adding a task increases a pet's task count.
- **Sorting:** out-of-order tasks come back chronologically; an earlier date sorts before a later one regardless of time.
- **Recurrence:** daily tasks repeat the next day and weekly tasks seven days later; a task completed early repeats after its due date; one-time tasks don't repeat; completing a task twice doesn't create a duplicate.
- **Conflicts:** two pets at the same date and time are flagged; the same time on different days is not; completed tasks are ignored.
- **Filtering and empty cases:** filtering by pet and/or completion status; an owner with no pets returns empty results without errors.

Recurrence tests build dates relative to `date.today()`, so they pass on any day.

Sample test output (`python -m pytest -v`):

```
collected 14 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 14%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 21%]
tests/test_pawpal.py::test_sort_by_time_puts_earlier_date_first PASSED   [ 28%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_copy PASSED [ 35%]
tests/test_pawpal.py::test_completing_weekly_task_creates_copy_seven_days_later PASSED [ 42%]
tests/test_pawpal.py::test_completing_future_task_early_counts_from_due_date PASSED [ 50%]
tests/test_pawpal.py::test_one_time_task_does_not_repeat PASSED          [ 57%]
tests/test_pawpal.py::test_completing_twice_does_not_duplicate PASSED    [ 64%]
tests/test_pawpal.py::test_conflict_between_two_pets_is_flagged PASSED   [ 71%]
tests/test_pawpal.py::test_same_time_on_different_days_is_not_a_conflict PASSED [ 78%]
tests/test_pawpal.py::test_completed_tasks_are_ignored_in_conflicts PASSED [ 85%]
tests/test_pawpal.py::test_filter_by_pet_and_by_status PASSED            [ 92%]
tests/test_pawpal.py::test_owner_with_no_pets_returns_empty_results PASSED [100%]

============================= 14 passed in 0.04s ==============================
```

**Confidence Level:** ★★★★☆ (4/5). All required scheduling behaviors and the main edge cases are tested, and deliberately breaking recurrence, the duplicate guard, or conflict detection makes the matching tests fail. The Streamlit UI is verified manually rather than by automated tests, and conflict detection only matches exact times, not overlapping durations.

## 📐 Smarter Scheduling

All scheduling logic lives in `pawpal_system.py`; `main.py` demonstrates each feature.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.todays_tasks()` | Sorts by due date, then time. Times are stored as zero-padded 24-hour `HH:MM` (enforced when a `Task` is created), so they sort correctly as text. |
| Filtering | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Filter by pet (case-insensitive), by completion status, by both, or neither. No matches, no pets, or no tasks return an empty list. Pet names are unique per owner. |
| Conflict handling | `Scheduler.find_conflicts()` | Flags incomplete tasks, for the same or different pets, that share the exact same date **and** time. Returns readable warnings instead of raising errors. Completed tasks are ignored, and durations are not checked for overlap. |
| Recurring tasks | `Scheduler.complete_task()`, `Task.next_occurrence()` | Completing a `daily` or `weekly` task keeps it as completed history and adds a new incomplete copy to the same pet, due `max(due date, today)` + 1 or 7 days. `once` tasks don't repeat. Completing an already-completed task does nothing, so no duplicates. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
