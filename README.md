# PawPal+

PawPal+ is a pet care planner for busy owners. You add your pets, schedule care tasks such as walks, feeding, medication, and vet visits, and PawPal+ shows today's plan in time order, warns you when two tasks are booked at the same time, and automatically schedules the next occurrence of daily and weekly tasks when you mark them done.

It has a Python backend (`pawpal_system.py`), a terminal demo (`main.py`), a Streamlit web app (`app.py`), and an automated test suite (`tests/test_pawpal.py`).

## Features

- **Pets and owner:** one owner with any number of pets; duplicate pet names are rejected.
- **Care tasks:** description, date, 24-hour time, duration, priority (low/medium/high), and frequency (once/daily/weekly). Invalid times, priorities, or frequencies are rejected.
- **Today's schedule:** today's tasks across all pets, sorted by time.
- **Filtering:** view tasks by pet, by completion status, or both.
- **Recurring tasks:** marking a daily or weekly task done keeps it as history and adds the next occurrence to the same pet.
- **Conflict warnings:** flags incomplete tasks that share the same date and time, for the same or different pets.
- **Priority and duration** are stored and displayed, but they do not change the order of the schedule.

## Getting started

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Tested with Python 3.13, Streamlit 1.60, and pytest 9.1.

### Run it

Run these from the project folder:

```bash
python main.py                    # terminal demo
python -m streamlit run app.py    # web app (opens in your browser)
python -m pytest                  # automated tests
```

## Architecture

All logic lives in `pawpal_system.py`, in four classes:

- `Task`: one care activity; validates its fields and can build its next occurrence.
- `Pet`: a pet and its own list of tasks.
- `Owner`: an owner's pets; collects every (pet, task) pair.
- `Scheduler`: works through the owner to sort, filter, complete, and check conflicts. It never keeps its own copy of the tasks, so it always sees current data.

`app.py` and `main.py` only call these methods; neither sorts, filters, or checks conflicts on its own.

- Final UML: [`diagrams/uml.mmd`](diagrams/uml.mmd)
- Original draft UML: [`diagrams/uml_draft.mmd`](diagrams/uml_draft.mmd)

## 🖥️ Sample Output

Output of `python main.py`. Tasks are added out of order, then the demo shows sorting, filtering, recurrence, and a deliberate conflict. Dates depend on the day you run it.

```
Today's Schedule for Jordan (Sunday, November 01, 2026)
-------------------------------------------------------
  07:30  Luna   Breakfast        (10 min, high)     [ ]
  08:00  Mochi  Morning walk     (30 min, high)     [ ]
  14:00  Luna   Vet checkup      (60 min, high)     [ ]
  18:30  Mochi  Evening walk     (30 min, medium)   [ ]

Filter: Mochi's tasks
---------------------
  08:00  Mochi  Morning walk     (30 min, high)     [ ]
  18:30  Mochi  Evening walk     (30 min, medium)   [ ]

Completed 'Morning walk'; next occurrence due Mon Nov 02 at 08:00.
Completing it a second time created: None (no duplicate).

Mochi's tasks after completion
------------------------------
  Sun Nov 01  08:00  Mochi  Morning walk     (30 min, high)     [x]
  Sun Nov 01  18:30  Mochi  Evening walk     (30 min, medium)   [ ]
  Mon Nov 02  08:00  Mochi  Morning walk     (30 min, high)     [ ]

Filter: incomplete tasks only
-----------------------------
  Sun Nov 01  07:30  Luna   Breakfast        (10 min, high)     [ ]
  Sun Nov 01  14:00  Luna   Vet checkup      (60 min, high)     [ ]
  Sun Nov 01  18:30  Mochi  Evening walk     (30 min, medium)   [ ]
  Mon Nov 02  08:00  Mochi  Morning walk     (30 min, high)     [ ]

Conflict check
--------------
  WARNING: Conflict on 2026-11-01 at 07:30: Luna - Breakfast, Luna - Medication
  (Grooming tomorrow at 18:30 is not flagged: same time as the evening walk, different day.)
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

Start the app with `python -m streamlit run app.py`, then:

1. **Set the owner.** Type a name in **Owner name**. The owner (and everything added below) stays in place as you use the page.
2. **Add pets.** In **Add a Pet**, enter a name and species and click **Add pet**, for example Mochi (dog) and Luna (cat). Adding a second pet with the same name shows an error instead of a duplicate.
3. **Schedule tasks.** In **Schedule a Task**, pick a pet and enter the task, date, 24-hour time, duration, priority, and how often it repeats. For example: Mochi, "Morning walk", today, 08:00, daily; and Luna, "Breakfast", today, 08:00, once.
4. **Read today's schedule.** **Today's Schedule** lists today's tasks in time order, whatever order they were added in. Because both tasks above are at 08:00 today, a ⚠️ warning names the date, the time, and both pets and tasks.
5. **Mark a recurring task done.** Click **Done** next to Mochi's Morning walk. A message confirms it and says the next walk is due tomorrow at 08:00. The walk shows ✅, and the conflict warning disappears because completed tasks don't count. Tomorrow's walk does not appear in Today's Schedule.
6. **Filter all tasks.** In **All Tasks**, choose a pet and/or a status (All, Incomplete, Completed). With Pet = Mochi you see today's completed walk and tomorrow's new walk; with Status = Incomplete only tasks still to do appear. If nothing matches, the app says so.

The same features are shown in the terminal in the **Sample Output** section above.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Limitations

- **Session-only data:** pets and tasks live in Streamlit's session state. Refreshing the page or restarting the app clears them; there is no file or database.
- **One owner per session**, and tasks cannot be edited or deleted after they are added.
- **Exact-time conflicts only:** a 60-minute task at 14:00 and another at 14:30 are not flagged.
- **No smart planning:** the schedule is ordered by time only. Priority, duration, and the owner's available time do not change the plan, and the app does not explain its choices.
