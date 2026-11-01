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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
