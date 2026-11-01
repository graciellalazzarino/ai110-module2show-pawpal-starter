"""PawPal+ terminal demo: builds a small household and prints today's schedule."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title: str, pairs: list[tuple[Pet, Task]]) -> None:
    """Print one readable line per (pet, task) pair."""
    print(title)
    print("-" * len(title))
    if not pairs:
        print("  (no tasks)")
    for pet, task in pairs:
        status = "[x]" if task.completed else "[ ]"
        details = f"({task.duration_minutes} min, {task.priority})"
        print(f"  {task.time}  {pet.name:<6} {task.description:<16} {details:<18} {status}")
    print()


def main() -> None:
    """Create an owner with two pets, add tasks out of order, and show today's schedule."""
    today = date.today()

    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of time order on purpose; the scheduler sorts them.
    mochi.add_task(Task("Evening walk", today, "18:30", 30, "medium", "daily"))
    luna.add_task(Task("Breakfast", today, "07:30", 10, "high", "daily"))
    mochi.add_task(Task("Morning walk", today, "08:00", 30, "high", "daily"))
    luna.add_task(Task("Vet checkup", today, "14:00", 60, "high", "once"))

    scheduler = Scheduler(owner)
    schedule = scheduler.sort_by_time(scheduler.todays_tasks())
    print_schedule(f"Today's Schedule for {owner.name} ({today:%A, %B %d, %Y})", schedule)


if __name__ == "__main__":
    main()
