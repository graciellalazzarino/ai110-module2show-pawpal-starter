"""PawPal+ backend: owners, pets, care tasks, and the scheduler that organizes them."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

PRIORITIES = ("low", "medium", "high")
FREQUENCIES = ("once", "daily", "weekly")


@dataclass
class Task:
    """One care activity for a pet, such as a walk, feeding, or medication."""

    description: str
    due_date: date
    time: str  # 24-hour "HH:MM", zero-padded (e.g. "08:00")
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", or "high"
    frequency: str = "once"  # "once", "daily", or "weekly"
    completed: bool = False

    def __post_init__(self) -> None:
        """Reject bad times, priorities, and frequencies as soon as a task is created."""
        try:
            datetime.strptime(self.time, "%H:%M")
            valid_time = len(self.time) == 5  # strptime alone would accept "8:00"
        except ValueError:
            valid_time = False
        if not valid_time:
            raise ValueError(f"time must be 24-hour HH:MM like '08:00', got {self.time!r}")
        if self.priority not in PRIORITIES:
            raise ValueError(f"priority must be one of {PRIORITIES}, got {self.priority!r}")
        if self.frequency not in FREQUENCIES:
            raise ValueError(f"frequency must be one of {FREQUENCIES}, got {self.frequency!r}")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next daily/weekly occurrence, or None for one-time tasks."""
        pass


@dataclass
class Pet:
    """A pet and its own list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """A pet owner who can have several pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner; raises ValueError if a pet with that name already exists."""
        for existing in self.pets:
            if existing.name.lower() == pet.name.lower():
                raise ValueError(f"{self.name} already has a pet named {existing.name!r}")
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all of this owner's pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Keep a reference to the owner so the scheduler always sees current pets and tasks."""
        self.owner = owner

    def todays_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs due today."""
        today = date.today()
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if task.due_date == today]

    def sort_by_time(self, pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return the pairs in chronological order."""
        # Zero-padded "HH:MM" strings sort the same way as the times they represent.
        return sorted(pairs, key=lambda pair: (pair[1].due_date, pair[1].time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> list[tuple[Pet, Task]]:
        """Return pairs matching the pet name and/or completion status; None means no filter."""
        pass

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete and add its next occurrence to the pet, if it recurs."""
        pass

    def find_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        pass
