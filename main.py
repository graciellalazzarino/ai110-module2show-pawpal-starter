"""PawPal+ terminal demo: builds a small household and shows the scheduler's features."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title: str, pairs: list[tuple[Pet, Task]], show_date: bool = False) -> None:
    """Print one readable line per (pet, task) pair."""
    print(title)
    print("-" * len(title))
    if not pairs:
        print("  (no tasks)")
    for pet, task in pairs:
        when = f"{task.due_date:%a %b %d}  {task.time}" if show_date else task.time
        details = f"({task.duration_minutes} min, {task.priority})"
        status = "[x]" if task.completed else "[ ]"
        print(f"  {when}  {pet.name:<6} {task.description:<16} {details:<18} {status}")
    print()


def main() -> None:
    """Create an owner with two pets and demonstrate sorting, filtering, recurrence, and conflicts."""
    today = date.today()
    tomorrow = today + timedelta(days=1)

    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of time order on purpose; the scheduler sorts them.
    mochi.add_task(Task("Evening walk", today, "18:30", 30, "medium", "daily"))
    luna.add_task(Task("Breakfast", today, "07:30", 10, "high", "daily"))
    morning_walk = Task("Morning walk", today, "08:00", 30, "high", "daily")
    mochi.add_task(morning_walk)
    luna.add_task(Task("Vet checkup", today, "14:00", 60, "high", "once"))

    scheduler = Scheduler(owner)

    # 1. Sorting
    schedule = scheduler.sort_by_time(scheduler.todays_tasks())
    print_schedule(f"Today's Schedule for {owner.name} ({today:%A, %B %d, %Y})", schedule)

    # 2. Filtering
    print_schedule("Filter: Mochi's tasks", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))

    # 3. Recurrence: completing a daily task creates tomorrow's copy for the same pet.
    next_walk = scheduler.complete_task(mochi, morning_walk)
    print(f"Completed '{morning_walk.description}'; next occurrence due {next_walk.due_date:%a %b %d} at {next_walk.time}.")
    again = scheduler.complete_task(mochi, morning_walk)
    print(f"Completing it a second time created: {again} (no duplicate).")
    print()
    print_schedule("Mochi's tasks after completion", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")), show_date=True)
    print_schedule("Filter: incomplete tasks only", scheduler.sort_by_time(scheduler.filter_tasks(completed=False)), show_date=True)

    # 4. Conflicts: Luna's medication is at the same time as Luna's breakfast today,
    #    and Luna's tomorrow grooming shares 18:30 with Mochi's evening walk (but on a different day).
    luna.add_task(Task("Medication", today, "07:30", 5, "high", "daily"))
    luna.add_task(Task("Grooming", tomorrow, "18:30", 20, "low", "once"))
    print("Conflict check")
    print("--------------")
    conflicts = scheduler.find_conflicts()
    for warning in conflicts:
        print(f"  WARNING: {warning}")
    if not conflicts:
        print("  No conflicts.")
    print("  (Grooming tomorrow at 18:30 is not flagged: same time as the evening walk, different day.)")


if __name__ == "__main__":
    main()
