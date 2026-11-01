"""Tests for the PawPal+ backend."""

from datetime import date

from pawpal_system import Pet, Task


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
