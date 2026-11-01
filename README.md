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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
