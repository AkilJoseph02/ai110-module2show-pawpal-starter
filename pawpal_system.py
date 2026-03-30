# PawPal System - A pet care management system

def time_to_str(minutes: int) -> str:
    """Convert minutes past midnight to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def minutes_to_hhmm(minutes: int) -> int:
    """Convert minutes past midnight to HHMM format."""
    hours = minutes // 60
    mins = minutes % 60
    return hours * 100 + mins

#Pet class represents a pet with attributes and methods to manage tasks.
class Pet:
    # Initialize a pet with given attributes and an empty task list.
    def __init__(self, name: str, species: str, breed: str, gender: str, weight: float, height: float, age: int, owner):
        self.name = name
        self.species = species
        self.breed = breed
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.owner = owner
        self.tasks = []  # List of tasks for this pet
    
    # Method to add a task to this pet's task list.
    def add_task(self, task: 'Task') -> bool:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)
            return True
        return False
    
    # Method to remove a task from this pet's task list.
    def remove_task(self, task: 'Task') -> bool:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False
    
    # Method to get all tasks assigned to this pet.
    def get_tasks(self) -> list:
        """Get all tasks assigned to this pet."""
        return self.tasks
    
    # Method to get tasks filtered by status for this pet.
    def get_tasks_by_status(self, status: str) -> list:
        """Get tasks filtered by status (pending, done, in-progress, aborted)."""
        return [task for task in self.tasks if task.status == status]
    
    # String representation of the pet for easy display.
    def __str__(self) -> str:
        return f"{self.name} ({self.species}, {self.breed}) - Age: {self.age}, Weight: {self.weight}lbs"

#Task class represents a task with attributes and methods to manage its status and associated pets.
class Task:
    @staticmethod
    def _normalize_start_time(start_time: int | None) -> int | None:
        """Convert HHMM inputs to minutes since midnight (24-hour)."""
        if start_time is None:
            return None
        if not isinstance(start_time, int):
            raise ValueError("start_time must be an integer in HHMM format")

        hours = start_time // 100
        minutes = start_time % 100
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return hours * 60 + minutes

        raise ValueError("start_time must be HHMM 0000-2359")

    # Initialize a task with given attributes and an optional list of pets.
    def __init__(self, description: str, start_time: int | None = None, duration: int = 1, pets: list = None, location: str = "", priority: int = 1, status: str = "pending", plan=None, frequency: str = "once"):
        if duration <= 0:
            raise ValueError("duration must be positive.")

        normalized_start = self._normalize_start_time(start_time)
        if normalized_start is not None and normalized_start + duration > 1440:
            raise ValueError("Task cannot extend past midnight (1440 minutes).")

        self.description = description
        self.start_time = normalized_start
        self.duration = duration
        self.location = location
        self.status = status
        self.priority = priority
        self.plan = plan  # Reference to parent plan
        self.pets = pets if pets is not None else []    # Pets involved in this task
        self.frequency = frequency  # 'once', 'daily', 'weekly', 'monthly'
    
    # Method to display the pets and their owner involved in this task.
    def display_pets_and_owner(self) -> str:
        """Display the pet(s) and their respective owner that are involved in the task."""
        if self.pets:
            pet_names = ", ".join([pet.name for pet in self.pets])
            owner_name = self.pets[0].owner.name if self.pets else "Unknown"
            result = f"Pets: {pet_names} | Owner: {owner_name}"
            print(result)
            return result
        else:
            result = "No pets assigned to this task"
            print(result)
            return result
    
    # Method to display the status of the task.
    def display_status(self) -> str:
        """Display status of the task (done/in progress/aborted)."""
        result = f"Task: {self.description} | Status: {self.status} | Priority: {self.priority}"
        print(result)
        return result
    
    # Method to add a pet to this task, ensuring bidirectional association.
    def add_pet(self, pet: 'Pet') -> bool:
        """Add a pet to this task. Returns True if successful, False otherwise."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.add_task(self)
            return True
        return False
    
    # Method to remove a pet from this task, ensuring bidirectional association.
    def remove_pet(self, pet: 'Pet') -> bool:
        """Remove a pet from this task. Returns True if successful, False otherwise."""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.remove_task(self)
            return True
        return False
    
    # Methods to change the status of the task.
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.status = "done"
        
        # If task is recurring, create next iteration
        if self.is_recurring() and self.start_time is not None:
            if self.frequency == "daily":
                offset = 1440  # 24 hours in minutes
            elif self.frequency == "weekly":
                offset = 10080  # 7 days in minutes
            else:
                return  # Handle other frequencies if needed
            
            new_start_minutes = (self.start_time + offset) % 1440
            new_start_hhmm = minutes_to_hhmm(new_start_minutes)
            
            # Create new task with same attributes
            new_task = Task(
                description=self.description,
                start_time=new_start_hhmm,
                duration=self.duration,
                pets=[],  # Will add pets below
                location=self.location,
                priority=self.priority,
                status="pending",
                plan=self.plan,
                frequency=self.frequency
            )
            
            # Add pets to new task (bidirectional association)
            for pet in self.pets:
                new_task.add_pet(pet)
            
            # Add to plan if exists
            if self.plan:
                self.plan.add_task(new_task)
    
    # Method to mark the task as in progress.
    def mark_in_progress(self) -> None:
        """Mark the task as in progress."""
        self.status = "in-progress"
    
    # Method to mark the task as aborted.
    def mark_aborted(self) -> None:
        """Mark the task as aborted."""
        self.status = "aborted"
    
    # Method to check if this task recurs based on its frequency.
    def is_recurring(self) -> bool:
        """Check if this task recurs."""
        return self.frequency != "once"
    
    # String representation of the task for easy display.
    def __str__(self) -> str:
        pets_str = ", ".join([p.name for p in self.pets]) if self.pets else "No pets"
        return f"{self.description} ({pets_str}) @ {self.location} | Status: {self.status} | Frequency: {self.frequency}"

#Owner class represents a pet owner with attributes and methods to manage their pets and tasks.
class Owner:
    # Initialize an owner with given attributes and an empty list of pets.
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.pets = []
    
    # Method to add a pet to this owner's collection.
    def add_pet(self, pet: 'Pet') -> bool:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)
            return True
        return False
    
    # Method to remove a pet from this owner's collection.
    def remove_pet(self, pet: 'Pet') -> bool:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)
            return True
        return False
    
    # Method to get all pets owned by this owner.
    def get_all_tasks(self) -> list:
        """Get all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    # Method to get all tasks for a specific pet.
    def get_tasks_by_pet(self, pet: 'Pet') -> list:
        """Get all tasks for a specific pet."""
        if pet in self.pets:
            return pet.get_tasks()
        return []
    
    # Method to get all tasks with a specific status across all pets.
    def get_tasks_by_status(self, status: str) -> list:
        """Get all tasks with a specific status across all pets."""
        matching_tasks = []
        for pet in self.pets:
            matching_tasks.extend(pet.get_tasks_by_status(status))
        return matching_tasks
    
    # Method to get all pending tasks across all pets.
    def get_pending_tasks(self) -> list:
        """Get all pending tasks across all pets."""
        return self.get_tasks_by_status("pending")
    
    # Method to get all completed tasks across all pets.
    def get_completed_tasks(self) -> list:
        """Get all completed tasks across all pets."""
        return self.get_tasks_by_status("done")
    
    # Method to assign a task for specific pets at given time/place, ensuring constraints are met.
    def assign_task(self, task: 'Task', pets: list, plan, time, location: str) -> bool:
        """
        Assign a task for specific pets at given time/place.
        Returns True if successful, False otherwise.
        """
        # Validate that all pets belong to this owner
        for pet in pets:
            if pet.owner != self:
                print(f"Error: Pet {pet.name} does not belong to {self.name}")
                return False
        
        # Check constraints before assigning
        if not plan.check_constraints(task, pets, time):
            print("Error: Task conflicts with existing schedule")
            return False
        
        # Add pets to the task
        for pet in pets:
            task.add_pet(pet)
        
        # Add task to the plan
        task.plan = plan
        plan.tasks.append(task)
        return True
    
    # Method to list all pets owned by this owner.
    def list_pets(self) -> None:
        """Display all pets owned by this owner."""
        print(f"\n{self.name}'s Pets ({len(self.pets)}):")
        for pet in self.pets:
            print(f"  - {pet}")
    
    # String representation of the owner for easy display.
    def __str__(self) -> str:
        return f"{self.name} ({self.age} years old) - {len(self.pets)} pet(s)"

#Plan class represents a care plan for an owner, managing tasks and ensuring constraints are met.
class Plan:
    # Initialize a plan for a specific owner with an empty task list and pet list.
    def __init__(self, owner: Owner):
        self.tasks = []
        self.pets = []
        self.owner = owner
    
    # Method to create a plan that best suits the owner on how they want to take care of their pets.
    def create_plan(self) -> dict:
        """
        Create a plan that best suits the owner on how they want to take care of their pets.
        Returns organized plan structure.
        """
        plan_structure = {
            "owner": self.owner.name,
            "pets": len(self.owner.pets),
            "total_tasks": len(self.tasks),
            "tasks_by_status": {
                "pending": len(self.owner.get_pending_tasks()),
                "completed": len(self.owner.get_completed_tasks()),
                "in-progress": len([t for t in self.tasks if t.status == "in-progress"]),
                "aborted": len([t for t in self.tasks if t.status == "aborted"])
            }
        }
        return plan_structure
    
    # Method to add a task to the plan, ensuring no duplicates and proper association.
    def add_task(self, task: 'Task') -> bool:
        """Add a task to the plan."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.plan = self
            return True
        return False
    
    # Method to remove a task from the plan, ensuring proper disassociation.
    def remove_task(self, task: 'Task') -> bool:
        """Remove a task from the plan."""
        if task in self.tasks:
            self.tasks.remove(task)
            task.plan = None
            return True
        return False
    
    # Method to check for constraints (time overlaps, availability, etc.) before assigning a task.
    def check_constraints(self, new_task: 'Task', pets: list, time) -> bool:
        """
        Check for constraints (time overlaps, availability, etc.).
        Returns True if task can be added, False otherwise.
        """
        new_pets = set(pets)

        # Check time-based conflicts for shared pets and reserve recovery gap
        for existing_task in self.tasks:
            if existing_task is new_task:
                continue
            if existing_task.status in ["done", "aborted"] or existing_task.start_time is None:
                continue

            existing_pets = set(existing_task.pets)
            if not existing_pets & new_pets:
                continue

            # Same pet is used by both tasks.
            if self._times_overlap(existing_task, new_task):
                return False

            # Same start time conflict (redundant with overlap but explicit rule preserved)
            if existing_task.start_time == time:
                return False

            # Require 30 min rest between tasks for same pet
            existing_end = existing_task.start_time + existing_task.duration
            if abs(existing_end - time) < 30:
                return False

        # Check max tasks per pet per day
        for pet in pets:
            pet_tasks_today = [t for t in self.get_tasks_by_pet(pet) if t.status not in ["done", "aborted"]]
            if len(pet_tasks_today) >= 5:
                return False

        return True
    
    # Helper method to check if two tasks have overlapping times.
    def _times_overlap(self, task1: 'Task', task2: 'Task') -> bool:
        """Helper method to check if two tasks have overlapping times."""
        try:
            task1_end = task1.start_time + task1.duration
            task2_end = task2.start_time + task2.duration
            return not (task1_end <= task2.start_time or task2_end <= task1.start_time)
        except (TypeError, AttributeError):
            return False
    
    # Method to get all tasks for a specific pet in this plan.
    def get_tasks_by_pet(self, pet: 'Pet') -> list:
        """Get all tasks for a specific pet in this plan."""
        return [task for task in self.tasks if pet in task.pets]
    
    # Method to get all tasks within a specific time range.
    def get_tasks_by_time(self, start_time, end_time) -> list:
        """Get all tasks within a specific time range."""
        return [task for task in self.tasks 
                if task.start_time >= start_time and task.start_time + task.duration <= end_time]
    
    # Method to get all tasks with a specific status in this plan.
    def get_tasks_by_status(self, status: str) -> list:
        """Get all tasks with a specific status."""
        return [task for task in self.tasks if task.status == status]
    
    # Method to get all tasks with a specific priority level in this plan.
    def get_tasks_by_priority(self, priority: int) -> list:
        """Get all tasks with a specific priority level."""
        return [task for task in self.tasks if task.priority == priority]
    
    # Method to get tasks filtered by completion status.
    def get_tasks_by_completion_status(self, completed: bool) -> list:
        """Get tasks filtered by completion status. If completed=True, return done tasks; if False, return non-done tasks."""
        if completed:
            return [task for task in self.tasks if task.status == "done"]
        else:
            return [task for task in self.tasks if task.status != "done"]
    
    # Method to get tasks filtered by pet name.
    def get_tasks_by_pet_name(self, pet_name: str) -> list:
        """Get tasks that involve a pet with the specified name."""
        return [task for task in self.tasks if any(pet.name == pet_name for pet in task.pets)]
    
    # Method to get conflicts in the plan.
    def get_conflicts(self) -> list:
        """Get a list of conflicts in the plan. Returns list of dicts with conflict details."""
        conflicts = []
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks):
                if i >= j:  # Avoid duplicate pairs and self-comparison
                    continue
                # Skip completed or aborted tasks
                if task1.status in ["done", "aborted"] or task2.status in ["done", "aborted"]:
                    continue
                if self._times_overlap(task1, task2):
                    shared_pets = set(task1.pets) & set(task2.pets)
                    if shared_pets:
                        # Same pet at same time
                        conflicts.append({
                            "type": "same_pet_same_time",
                            "tasks": [task1, task2],
                            "shared_pets": list(shared_pets),
                            "description": f"Tasks '{task1.description}' and '{task2.description}' involve the same pet(s) {', '.join(p.name for p in shared_pets)} at overlapping times."
                        })
                    else:
                        # Different pets overlapping
                        conflicts.append({
                            "type": "different_pets_overlap", 
                            "tasks": [task1, task2],
                            "pet_groups": [task1.pets, task2.pets],
                            "description": f"Tasks '{task1.description}' and '{task2.description}' involve different pets at overlapping times."
                        })
        return conflicts
    
    def get_available_time_slots(self, pet: 'Pet', duration: int) -> list:
        """
        Get available time slots for a pet.
        Returns a list of tasks that the pet is already assigned to.
        """
        occupied_slots = [task for task in self.tasks if pet in task.pets and task.status != "aborted"]
        return occupied_slots
    
    # Method to sort all tasks by priority level (highest first).
    def sort_tasks_by_priority(self) -> list:
        """Sort all tasks by priority level (highest first)."""
        return sorted(self.tasks, key=lambda t: t.priority, reverse=True)
    
    # Method to sort all tasks by start time.
    def sort_tasks_by_time(self) -> list:
        """Sort all tasks by start time."""
        return sorted(
            self.tasks,
            key=lambda t: (t.start_time is None, t.start_time if t.start_time is not None else float('inf')),
        )

    def schedule_tasks(self) -> bool:
        """Automatically schedule tasks by priority (lower number = higher priority)."""
        fixed_tasks = [t for t in self.tasks if t.start_time is not None]
        unscheduled_tasks = [t for t in self.tasks if t.start_time is None]

        # Validate all fixed tasks first.
        for task in fixed_tasks:
            if not self.check_constraints(task, task.pets, task.start_time):
                return False

        # Assign unscheduled tasks to first available 30-min slots.
        for task in sorted(unscheduled_tasks, key=lambda t: t.priority):
            assigned = False
            candidate = 0
            while candidate <= 1440 - task.duration:
                if self.check_constraints(task, task.pets, candidate):
                    task.start_time = candidate
                    assigned = True
                    break
                candidate += 30
            if not assigned:
                return False

        return True

    def edit_plan(self, task: 'Task', new_description: str = None, new_status: str = None) -> bool:
        """
        Allow a plan to be edited.
        Returns True if successful, False otherwise.
        """
        if task in self.tasks:
            if new_description:
                task.description = new_description
            if new_status:
                task.status = new_status
            return True
        return False
    
    # Method to delete the entire plan, clearing all tasks and pet associations.
    def delete_plan(self) -> None:
        """Allow a plan to be deleted."""
        self.tasks.clear()
        self.pets.clear()
    
    # Method to generate a formatted schedule of all tasks in the plan.
    def generate_schedule(self) -> str:
        """Generate a formatted schedule of all tasks."""
        schedule = f"\n=== Schedule for {self.owner.name} ===\n"
        sorted_tasks = self.sort_tasks_by_time()
        
        if not sorted_tasks:
            schedule += "No tasks scheduled.\n"
            return schedule
        
        for task in sorted_tasks:
            pets_str = ", ".join([p.name for p in task.pets]) if task.pets else "No pets"
            if task.start_time is not None:
                start_str = time_to_str(task.start_time)
                end_str = time_to_str(task.start_time + task.duration)
            else:
                start_str = "Unscheduled"
                end_str = "Unscheduled"
            schedule += f"[{task.status.upper()}] {task.description}\n"
            schedule += f"  Time: {start_str} - {end_str} ({task.duration} min)\n"
            schedule += f"  Pets: {pets_str}\n"
            schedule += f"  Location: {task.location} | Priority: {task.priority}\n\n"
        
        return schedule
    
    # Method to get a summary of the plan, including total tasks and counts by status.
    def get_summary(self) -> str:
        """Get a summary of the plan."""
        summary = f"\nPlan Summary for {self.owner.name}:\n"
        summary += f"  Total Tasks: {len(self.tasks)}\n"
        summary += f"  Pending: {len(self.get_tasks_by_status('pending'))}\n"
        summary += f"  In Progress: {len(self.get_tasks_by_status('in-progress'))}\n"
        summary += f"  Completed: {len(self.get_tasks_by_status('done'))}\n"
        summary += f"  Aborted: {len(self.get_tasks_by_status('aborted'))}\n"
        return summary

    def warning_message(self) -> str:
        """Produce a warning string for Streamlit based on schedule state."""
        if not self.tasks:
            return "No scheduled tasks yet. Add tasks and click Generate schedule."
        return f"Schedule generated: {len(self.tasks)} task(s) in plan."

    def schedule_markdown(self) -> str:
        """Produce markdown for schedule display."""
        if not self.tasks:
            return "### No tasks scheduled yet."

        md = f"### Schedule for {self.owner.name}\n"
        for task in self.sort_tasks_by_time():
            pets_str = ", ".join([p.name for p in task.pets]) if task.pets else "No pets"
            md += f"- **{task.description}**\n"
            if task.start_time is not None:
                start_str = time_to_str(task.start_time)
                end_str = time_to_str(task.start_time + task.duration)
            else:
                start_str = "Unscheduled"
                end_str = "Unscheduled"
            md += f"  - Time: {start_str} - {end_str} ({task.duration} min)\n"
            md += f"  - Pets: {pets_str}\n"
            md += f"  - Location: {task.location}\n"
            md += f"  - Status: {task.status}\n"
            md += f"  - Priority: {task.priority}\n"
            md += f"  - Frequency: {task.frequency}\n\n"
        md += self.get_summary().replace("\n", "\\n") if False else ""
        return md
