from pawpal_system import Pet
from pawpal_system import Owner
from pawpal_system import Task
from pawpal_system import Plan


def main():
    # Create an owner
    Jon = Owner(name="John Arbuckle", age=25, gender="male")
    

    # Create pets and add them to the owner
    Odie = Pet(name="Odie", species="dog", breed='Golden Retriever', gender="male", weight=30.0, height=20.0, age=5, owner=Jon)
    Garfield = Pet(name="Garfield", species="cat", breed='Tabby', gender="male", weight=50.0, height=10.0, age=7, owner=Jon)
    
    Jon.add_pet(Odie)
    Jon.add_pet(Garfield)
    

    # Create a plan for the day
    daily_plan = Plan(owner=Jon)
    

    # Create some tasks for the pets
    task2 = Task(description="Take Odie for a walk", start_time=800, duration=30, location="Park", priority=1, pets=[Odie])
    task3 = Task(description="Feed Garfield", start_time=1000, duration=5, location="Kitchen", priority=2, pets=[Garfield])
    task1 = Task(description="Play with Odie", start_time=1300, duration=20, location="Living Room", priority=3, pets=[Odie])
    task4 = Task(description="Groom Garfield", start_time=800, duration=15, location="Bathroom", priority=1, pets=[Garfield])
    

    # Add tasks to the plan
    daily_plan.add_task(task1)
    daily_plan.add_task(task2)
    daily_plan.add_task(task3)
    daily_plan.add_task(task4)
    
    # Automatically schedule tasks
    if not daily_plan.schedule_tasks():
        print("Warning: Could not schedule all tasks without conflicts.")
    
    # Check for conflicts
    conflicts = daily_plan.get_conflicts()
    if conflicts:
        print(f"\nWarning: Found {len(conflicts)} scheduling conflict(s):")
        for conflict in conflicts:
            print(f"  - {conflict['description']}")
    
    

    # Display owner and their pets
    print(f"\n{Jon}")
    Jon.list_pets()


    # Display the plan
    print(daily_plan.generate_schedule())
    print(daily_plan.get_summary())


    # Display individual task details
    print("\n=== Task Details ===")
    for task in daily_plan.sort_tasks_by_time():
        task.display_status()
        task.display_pets_and_owner()
        print()  # Add blank line between tasks


if __name__ == "__main__":
    main()