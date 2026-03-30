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
    def __init__(self, description: str, start_time, duration: int, location: str, priority: int, status: str = "pending"):
        self.description = description
        self.start_time = start_time
        self.duration = duration
        self.location = location
        self.status = status
        self.priority = priority
    
    def display_pets_and_owner(self):
        """Display the pet(s) and their respective owner that are involved in the task."""
        pass
    
    def display_status(self):
        """Display status of the task (done/in progress/aborted)."""
        pass


class Owner:
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.pets = []
    
    def assign_task(self, task: Task, pet: Pet, time, location: str):
        """Assign a task for a specific pet at given time/place."""
        pass


class Plan:
    def __init__(self, owner: Owner):
        self.tasks = []
        self.pets = []
        self.owner = owner
    
    def create_plan(self):
        """Create a plan that best suits the owner on how they want to take care of their pets."""
        pass
    
    def check_constraints(self):
        """Check for constraints (time overlaps, availability, etc.)."""
        pass
    
    def edit_plan(self):
        """Allow a plan to be edited."""
        pass
    
    def delete_plan(self):
        """Allow a plan to be deleted."""
        pass
