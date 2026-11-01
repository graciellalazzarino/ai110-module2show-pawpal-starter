# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. Schedule a care task: add a task such as a walk or medication to a pet, with its date, time, duration, priority, and how often it repeats.
2. View today's plan: see today's tasks across all pets, sorted by time, with any time conflicts flagged.
3. Mark a task complete: check off a task; daily or weekly tasks automatically get their next occurrence.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML (`diagrams/uml_draft.mmd`) has four classes. An `Owner` has zero or more `Pet`s, each `Pet` has zero or more `Task`s, and a `Scheduler` holds a reference to one `Owner` and reaches every pet and task through it instead of keeping its own copy.

- `Task`: one care activity, storing its description, due date, 24-hour `HH:MM` time, duration, priority, frequency (once/daily/weekly), and whether it is completed. It can mark itself complete and build its next occurrence.
- `Pet`: a pet's name and species plus its own list of tasks; it can add a task.
- `Owner`: the owner's name and list of pets; it can add a pet and collect every (pet, task) pair across all pets.
- `Scheduler`: gets today's tasks, sorts them by time, filters by pet and/or completion status, completes tasks (adding the next occurrence for recurring ones), and finds tasks scheduled at the same date and time.

I gave tasks a date as well as a time because recurrence and "today's plan" need to tell days apart. Completion goes through the `Scheduler` because a `Task` does not know which pet it belongs to, so it cannot add its own next occurrence to that pet's list.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. After reviewing the skeleton, I added three rules:

- `Task` now rejects a time that is not zero-padded 24-hour `HH:MM` (for example `"8:00"` or `"2:30 PM"`). Times are compared as strings, so `"8:00"` would sort after `"10:00"`.
- `Task` only accepts the priorities low/medium/high and the frequencies once/daily/weekly, so a typo such as `"Daily"` cannot silently break recurrence.
- `Owner.add_pet()` will refuse a second pet with the same name, so filtering by pet name always means one pet.

I rejected two suggestions: returning structured conflict objects instead of warning strings, because strings already identify the pets, tasks, and time; and caching `get_all_tasks()`, because with a few pets it is already instant and a cache could go out of date when a task is added.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers each task's date and time, whether it is completed, and which pet it belongs to. Today's plan only includes tasks due today, sorted by time; completed tasks stay visible as history but no longer count toward conflicts; and recurring tasks are scheduled forward from the later of their due date and today. Each task also stores a priority and a duration, but they are only displayed and do not change the order of the plan.

I put date and time first because the core user actions (scheduling a task, viewing today's plan, and marking tasks complete) all depend on knowing exactly when a task happens. Priority-based ordering and fitting tasks into the owner's available time were left out to keep the scheduler small and easy to verify.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

When a daily or weekly task is completed, the next occurrence is due on the later of the task's due date and today, plus 1 or 7 days. The assignment's example uses "today + 1 day," and I considered "due date + 1 day" as well. Each simple rule has a problem: with "today + 1," completing tomorrow's walk early today creates a second walk on the same day as the original; with "due date + 1," finishing an overdue task creates a next task that is already overdue. Taking the later of the two dates gives the same result as "today + 1" whenever a task is completed on time or late, and avoids the duplicate when it is completed early.

The tradeoff is that the rule is harder to explain in one sentence, and a pet does not keep a fixed rhythm (for example, every Monday) after a weekly task is done late; the schedule shifts to count from the day it was actually done. That is reasonable here because a busy owner mainly needs the next reminder to land on a sensible future day and never be duplicated, not to keep a strict calendar pattern.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used one AI coding assistant (Claude Code) for the whole project, working in small batches: it proposed a plan, I approved or changed it, it made the change and showed the results, and I reviewed before each commit. The most useful help was explaining concepts as they came up (dataclasses, `field(default_factory=list)`, `sorted()` with a key, `timedelta`, and Streamlit's `session_state`), the step-by-step review process, and debugging. For example, when the app crashed with `'NoneType' object is not iterable`, the cause turned out to be an old Streamlit server still running code from before `find_conflicts()` was implemented, not a bug in the code. The assignment suggests separate chats for algorithm planning and testing; I did not use separate chats and kept everything in one session.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When reviewing the class skeleton, the AI suggested five changes. I accepted three (time format checks, allowed priority/frequency values, and no duplicate pet names) and rejected two: caching `get_all_tasks()`, because with a few pets it is already fast and a cache could go out of date, and returning structured conflict objects, because plain warning messages already name the pets, tasks, and time. For recurrence, I also chose the "later of due date and today" rule instead of using the assignment's plain "today + 1" as-is.

I verified the AI's work by running `python main.py` and `python -m pytest` myself, walking through the Streamlit app by hand, and reviewing the changes before each commit. That mattered: the AI made real mistakes during the project, such as a demo script that crashed with an `IndexError` and an edit that broke the UML file, and those were only caught because the code was actually run and checked.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The 14 tests in `tests/test_pawpal.py` cover marking tasks complete and adding tasks; sorting by time and by date; daily and weekly recurrence, early completion, one-time tasks, and completing a task twice; conflicts between two pets, the same time on different days, and completed tasks being ignored; filtering by pet and status; and an owner with no pets.

These are the behaviors the schedule depends on. A wrong sort or a missed conflict would give the owner a misleading plan, and recurrence bugs are easy to miss by hand because they only show up on later days. The edge cases (duplicates, empty data, same time on different days) are where simple code most often goes wrong.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

4 out of 5 stars. All 14 automated tests pass, and when recurrence, the duplicate-completion guard, and conflict detection were deliberately broken, the matching tests failed. The Streamlit UI was only checked by hand, and conflicts only match exact times.

Next I would test: tasks whose durations overlap without sharing a start time (currently not flagged by design), recurrence across month and year boundaries with fixed dates, invalid input through the UI forms, and automated tests for the Streamlit UI, such as clicking Done on a recurring task.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The UI interaction. In the Streamlit app you can add pets and tasks, see today's schedule sorted with conflict warnings, click Done on a recurring task and immediately see the next one scheduled for the following day, and filter all tasks by pet and status, all using the same backend methods as the terminal demo.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would detect overlapping tasks, not just tasks with the exact same start time. Right now a 60-minute task at 14:00 and another at 14:30 are not flagged, even though they overlap. I would also look at efficiency, for example how the scheduler rebuilds the full task list on every call, which is fine for a few pets but would not scale well.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Verify, don't trust. The AI's code and explanations were usually right, but not always: it wrote a demo that crashed, and one of its edits broke a file. Running the code, reading the output, and testing the app myself is what caught those problems, so I can't treat AI output as finished until I've checked it.
