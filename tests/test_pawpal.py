"""Tests for the PawPal+ backend."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

TODAY = date.today()
FIXED_DAY = date(2026, 11, 1)


def make_household():
    """Return (owner, mochi, luna, scheduler) with two pets and no tasks."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner, mochi, luna, Scheduler(owner)


# --- Initial tests ---------------------------------------------------------


def test_mark_complete_changes_status():
    """A new task starts incomplete and is complete after mark_complete()."""
    task = Task("Morning walk", date(2026, 11, 1), "08:00", 30)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet increases that pet's task count by one."""
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Breakfast", date(2026, 11, 1), "07:30", 10))

    assert len(pet.tasks) == 1


# --- Sorting ---------------------------------------------------------------


def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order come back earliest first."""
    owner, mochi, luna, scheduler = make_household()
    mochi.add_task(Task("Evening walk", FIXED_DAY, "18:30", 30))
    luna.add_task(Task("Breakfast", FIXED_DAY, "07:30", 10))
    mochi.add_task(Task("Vet", FIXED_DAY, "14:00", 60))

    times = [task.time for _, task in scheduler.sort_by_time(owner.get_all_tasks())]

    assert times == ["07:30", "14:00", "18:30"]


def test_sort_by_time_puts_earlier_date_first():
    """A late task today sorts before an early task tomorrow."""
    owner, mochi, _, scheduler = make_household()
    mochi.add_task(Task("Tomorrow breakfast", FIXED_DAY + timedelta(days=1), "07:00", 10))
    mochi.add_task(Task("Tonight walk", FIXED_DAY, "20:00", 30))

    names = [task.description for _, task in scheduler.sort_by_time(owner.get_all_tasks())]

    assert names == ["Tonight walk", "Tomorrow breakfast"]


# --- Recurrence ------------------------------------------------------------


def test_completing_daily_task_creates_next_day_copy():
    """Completing a daily task due today adds an incomplete copy due tomorrow to the same pet."""
    _, mochi, _, scheduler = make_household()
    walk = Task("Morning walk", TODAY, "08:00", 30, "high", "daily")
    mochi.add_task(walk)

    next_walk = scheduler.complete_task(mochi, walk)

    assert walk.completed is True
    assert next_walk in mochi.tasks
    assert next_walk.completed is False
    assert next_walk.due_date == TODAY + timedelta(days=1)
    assert (next_walk.description, next_walk.time, next_walk.frequency) == ("Morning walk", "08:00", "daily")


def test_completing_weekly_task_creates_copy_seven_days_later():
    """Completing a weekly task due today adds a copy due in seven days."""
    _, mochi, _, scheduler = make_household()
    bath = Task("Bath", TODAY, "10:00", 20, "low", "weekly")
    mochi.add_task(bath)

    next_bath = scheduler.complete_task(mochi, bath)

    assert next_bath.due_date == TODAY + timedelta(days=7)


def test_completing_future_task_early_counts_from_due_date():
    """A daily task completed before its due date repeats the day after its due date, not tomorrow."""
    _, mochi, _, scheduler = make_household()
    due = TODAY + timedelta(days=5)
    walk = Task("Morning walk", due, "08:00", 30, "high", "daily")
    mochi.add_task(walk)

    next_walk = scheduler.complete_task(mochi, walk)

    assert next_walk.due_date == due + timedelta(days=1)


def test_one_time_task_does_not_repeat():
    """Completing a one-time task adds no new task."""
    _, _, luna, scheduler = make_household()
    vet = Task("Vet checkup", TODAY, "14:00", 60, "high", "once")
    luna.add_task(vet)

    result = scheduler.complete_task(luna, vet)

    assert result is None
    assert vet.completed is True
    assert len(luna.tasks) == 1


def test_completing_twice_does_not_duplicate():
    """Completing an already-completed task returns None and adds nothing."""
    _, mochi, _, scheduler = make_household()
    walk = Task("Morning walk", TODAY, "08:00", 30, "high", "daily")
    mochi.add_task(walk)
    scheduler.complete_task(mochi, walk)

    second = scheduler.complete_task(mochi, walk)

    assert second is None
    assert len(mochi.tasks) == 2  # the original plus one next occurrence


# --- Conflicts -------------------------------------------------------------


def test_conflict_between_two_pets_is_flagged():
    """Two pets with tasks at the same date and time produce one warning naming both."""
    _, mochi, luna, scheduler = make_household()
    mochi.add_task(Task("Morning walk", FIXED_DAY, "08:00", 30))
    luna.add_task(Task("Breakfast", FIXED_DAY, "08:00", 10))

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Mochi" in warnings[0] and "Luna" in warnings[0]


def test_same_time_on_different_days_is_not_a_conflict():
    """Identical clock times on different dates are not flagged."""
    _, mochi, luna, scheduler = make_household()
    mochi.add_task(Task("Morning walk", FIXED_DAY, "08:00", 30))
    luna.add_task(Task("Breakfast", FIXED_DAY + timedelta(days=1), "08:00", 10))

    assert scheduler.find_conflicts() == []


def test_completed_tasks_are_ignored_in_conflicts():
    """A clash where one task is already completed is not flagged."""
    _, mochi, luna, scheduler = make_household()
    walk = Task("Morning walk", FIXED_DAY, "08:00", 30)
    mochi.add_task(walk)
    luna.add_task(Task("Breakfast", FIXED_DAY, "08:00", 10))
    walk.mark_complete()

    assert scheduler.find_conflicts() == []


# --- Filtering and empty cases --------------------------------------------


def test_filter_by_pet_and_by_status():
    """Filtering by pet returns only that pet's tasks; completed=False returns only incomplete ones."""
    _, mochi, luna, scheduler = make_household()
    walk = Task("Morning walk", FIXED_DAY, "08:00", 30)
    mochi.add_task(walk)
    mochi.add_task(Task("Evening walk", FIXED_DAY, "18:30", 30))
    luna.add_task(Task("Breakfast", FIXED_DAY, "07:30", 10))
    walk.mark_complete()

    assert {pet.name for pet, _ in scheduler.filter_tasks(pet_name="mochi")} == {"Mochi"}
    assert len(scheduler.filter_tasks(pet_name="Mochi")) == 2
    assert all(not task.completed for _, task in scheduler.filter_tasks(completed=False))
    assert len(scheduler.filter_tasks(completed=False)) == 2
    assert [task.description for _, task in scheduler.filter_tasks(pet_name="Mochi", completed=False)] == ["Evening walk"]


def test_owner_with_no_pets_returns_empty_results():
    """With no pets, every scheduler method returns an empty list instead of failing."""
    scheduler = Scheduler(Owner("Jordan"))

    assert scheduler.todays_tasks() == []
    assert scheduler.sort_by_time(scheduler.todays_tasks()) == []
    assert scheduler.filter_tasks(pet_name="Mochi") == []
    assert scheduler.find_conflicts() == []
