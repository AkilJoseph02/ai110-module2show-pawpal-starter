# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Contains the following actions that the application should be able to do:
    1. Add a pet in, so that the owner can have each task be related to a specific pet.
    2. See a task for the day for all of the owner's pets (like an overview).
    3. Create tasks with their own descriptions, time, duration, etc.
- What classes did you include, and what responsibilities did you assign to each?
    1. Pet:
       Attributes:
        a. Species
        b. Breed
        c. Gender
        d. Weight and Height
        e. Name
        f. Age
        g. Owner
       Methods:
        None
    2. Tasks:
       Attributes:
        a. Description/Name
        b. Start time
        c. Duration
        d. Location
        e. Status (If task was done or not, if the task was delayed, etc.)
        f. Priority
       Methods:
        a. Display the pet(s) and their respective owner that are involved in the task.
        b. Display status of said task to show if it was done/in progress/aborted.
    3. Owner:
       Attributes:
        a. Name
        b. Age
        c. Gender
        b. List of pets they own.
       Methods:
        a. Assign a task for a specific pet at given time/place.
    4. Plan:
       Attributes:
        a. List of Tasks
        b. Pets involved.
        c. Owner the plan belongs to.
       Methods:
        a. Create a plan that best suits the owner on how they want to take care of their pets.
        b. Check for constraints while creating said plan (if this task overlaps with another in time, if a pet or the owner are available for doing a certain task at a given time, etc.)
        c. Allow a plan to be editted.
        d. Allow a plan to be deleted.

**b. Design changes**

- Did your design change during implementation?
    Answer: Yes.
- If yes, describe at least one change and why you made it.
    Answer: Allowed the plan class to track parent plan (in cases where a plan is appended to another), allowed the plan class to keep track of which pets are involved and which owner they belong to. Allowed the Plan class to check constraints before adding in tasks. I allowed these changes to go through because they're necessary in making a functional plan for pets (keeping of who/what's involved in said plan and making sure there's no overlap).

    The changes made sense to add.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
