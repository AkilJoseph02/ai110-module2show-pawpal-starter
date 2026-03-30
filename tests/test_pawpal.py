import unittest
import sys
sys.path.insert(0, '..')

from pawpal_system import Pet, Owner, Task, Plan


class TestTaskCompletion(unittest.TestCase):
    """Test that mark_complete() changes task status correctly."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner(name="Test Owner", age=30, gender="female")
        self.pet = Pet(name="Fluffy", species="cat", breed="Siamese", gender="female", 
                       weight=8.5, height=10.0, age=3, owner=self.owner)
        self.task = Task(description="Groom Fluffy", start_time=900, duration=300, 
                         location="Home", priority=2, pets=[self.pet])
    
    def test_mark_complete_changes_status(self):
        """Verify that mark_complete() changes status from pending to done."""
        # Initial status should be pending
        self.assertEqual(self.task.status, "pending")
        
        # Call mark_complete()
        self.task.mark_complete()
        
        # Status should now be done
        self.assertEqual(self.task.status, "done")
    
    def test_mark_in_progress_changes_status(self):
        """Verify that mark_in_progress() changes status appropriately."""
        self.task.mark_in_progress()
        self.assertEqual(self.task.status, "in-progress")
    
    def test_mark_aborted_changes_status(self):
        """Verify that mark_aborted() changes status to aborted."""
        self.task.mark_aborted()
        self.assertEqual(self.task.status, "aborted")


class TestTaskAddition(unittest.TestCase):
    """Test that adding a task to a Pet increases task count."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner(name="Test Owner", age=30, gender="male")
        self.pet = Pet(name="Max", species="dog", breed="Golden Retriever", gender="male", 
                       weight=65.0, height=24.0, age=5, owner=self.owner)
        self.task1 = Task(description="Take Max for a walk", start_time=800, duration=600, 
                          location="Park", priority=1)
        self.task2 = Task(description="Play with Max", start_time=1400, duration=900, 
                          location="Backyard", priority=2)
    
    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a pet increases task count."""
        # Initial task count should be 0
        self.assertEqual(len(self.pet.tasks), 0)
        
        # Add first task
        self.pet.add_task(self.task1)
        self.assertEqual(len(self.pet.tasks), 1)
        
        # Add second task
        self.pet.add_task(self.task2)
        self.assertEqual(len(self.pet.tasks), 2)
    
    def test_add_task_returns_true_on_success(self):
        """Verify that add_task returns True on successful addition."""
        result = self.pet.add_task(self.task1)
        self.assertTrue(result)
    
    def test_add_duplicate_task_returns_false(self):
        """Verify that adding duplicate task returns False."""
        self.pet.add_task(self.task1)
        result = self.pet.add_task(self.task1)  # Try to add same task again
        self.assertFalse(result)
        self.assertEqual(len(self.pet.tasks), 1)  # Count should still be 1
    
    def test_remove_task_decreases_pet_task_count(self):
        """Verify that removing a task decreases task count."""
        self.pet.add_task(self.task1)
        self.pet.add_task(self.task2)
        self.assertEqual(len(self.pet.tasks), 2)
        
        # Remove task
        self.pet.remove_task(self.task1)
        self.assertEqual(len(self.pet.tasks), 1)


if __name__ == "__main__":
    unittest.main()
