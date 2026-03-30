class Pet:
    def __init__(self, name: str, species: str, breed: str, gender: str, weight: float, height: float, age: int, owner):
        self.name = name
        self.species = species
        self.breed = breed
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.owner = owner


class Task:
    def __init__(self, description: str, start_time, duration: int, location: str, priority: int, status: str = "pending", plan=None):
        self.description = description
        self.start_time = start_time
        self.duration = duration
        self.location = location
        self.status = status
        self.priority = priority
        self.plan = plan  # Reference to parent plan
        self.pets = []    # Pets involved in this task
    
    def display_pets_and_owner(self):
        """Display the pet(s) and their respective owner that are involved in the task."""
        if self.pets:
            pet_names = ", ".join([pet.name for pet in self.pets])
            owner_name = self.pets[0].owner.name if self.pets else "Unknown"
            print(f"Pets: {pet_names} | Owner: {owner_name}")
        else:
            print("No pets assigned to this task")
    
    def display_status(self):
        """Display status of the task (done/in progress/aborted)."""
        print(f"Task: {self.description} | Status: {self.status}")
    
    def add_pet(self, pet: Pet) -> bool:
        """Add a pet to this task. Returns True if successful, False otherwise."""
        if pet not in self.pets:
            self.pets.append(pet)
            return True
        return False
    
    def remove_pet(self, pet: Pet) -> bool:
        """Remove a pet from this task. Returns True if successful, False otherwise."""
        if pet in self.pets:
            self.pets.remove(pet)
            return True
        return False


class Owner:
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.pets = []
    
    def add_pet(self, pet: Pet) -> bool:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)
            return True
        return False
    
    def assign_task(self, task: Task, pets: list, plan, time, location: str) -> bool:
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


class Plan:
    def __init__(self, owner: Owner):
        self.tasks = []
        self.pets = []
        self.owner = owner
    
    def create_plan(self):
        """Create a plan that best suits the owner on how they want to take care of their pets."""
        pass
    
    def check_constraints(self, new_task: Task, pets: list, time) -> bool:
        """
        Check for constraints (time overlaps, availability, etc.).
        Returns True if task can be added, False otherwise.
        """
        for existing_task in self.tasks:
            # Check if time slots overlap
            if self._times_overlap(existing_task, new_task):
                # Check if any shared pets exist
                existing_pets = set(existing_task.pets)
                new_pets = set(pets)
                if existing_pets & new_pets:  # If intersection is not empty
                    return False
        return True
    
    def _times_overlap(self, task1: Task, task2: Task) -> bool:
        """Helper method to check if two tasks have overlapping times."""
        task1_end = task1.start_time + task1.duration
        task2_end = task2.start_time + task2.duration
        return not (task1_end <= task2.start_time or task2_end <= task1.start_time)
    
    def get_available_time_slots(self, pet: Pet, duration: int) -> list:
        """
        Get available time slots for a pet.
        Returns a list of available time slots with sufficient duration.
        """
        occupied_slots = [task for task in self.tasks if pet in task.pets]
        # This is a simplified version; a full implementation would show actual available slots
        return occupied_slots
    
    def edit_plan(self, task: Task, new_description: str = None, new_status: str = None) -> bool:
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
    
    def delete_plan(self):
        """Allow a plan to be deleted."""
        self.tasks.clear()
        self.pets.clear()
