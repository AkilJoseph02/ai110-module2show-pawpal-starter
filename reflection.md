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
Answer: Considers if task involving the same/different pets overlap.
- How did you decide which constraints mattered most?
Answer: I figured that that the time constraints would be the most important, considering that the entire point of Pawpal is to consider the amount of time a pet owner has to care for their pets, and creating a plan to efficiently use all that time to ensure that the owner can give sufficient care.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Answer: Haven't factored how deal with preference of the owner yet. Figured making sure that there are no conflicts with pet tasks was more important than making a plan hyper-specialized to the owner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
Answer: Being descript and including as much detail as possible helped create the most helpful prompts. Otherwise, the AI would wander off from I wanted it to do.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Answer: One moment was when I was working on the start time attribute of tasks. The AI got some units mixed because the input for the time was integers, so it assumed that if the start time of a task was set to "0800", instead of assuming that it meant 8:00AM, it thought that 800 was just the amount of minutes.
- How did you evaluate or verify what the AI suggested?
Answer: By going through the conflict restraints, that's when I noticed that the AI messed some things up. After being more thorough with my prompts and mentioning that I wanted the start times to be in the 24 clock format (made it easier to deal with logic instead of having to deal with extra logic to account for AM and PM times), I got it working again.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
If the app would see that conflicts between tasks arose if there involved the same pets and happened around the same time, cases where the task would go into the next day, etc.
- Why were these tests important?
Answer: They're important because they're meant account for extreme cases that are unordinary, but still require the application to function appropriately instead of crashing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
Answer: 4 out of 5
- What edge cases would you test next if you had more time?
Answer: If an owner tried to do a task without a pet involved, how to deal with several tasks starting at the same time with the same priority, etc.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Creating the classes needed for the project's skeleton and working on the application's ability to detect task conflicts while creating plans.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Answer: Use more edge cases in testing.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Answer: Have a thorough and carefully explained base/skeleton before using AI to help implement logic and code for a project. AI can be pretty aimless without the necessary guidance and instruction.