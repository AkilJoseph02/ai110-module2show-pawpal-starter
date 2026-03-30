import streamlit as st
from pawpal_system import Pet
from pawpal_system import Owner
from pawpal_system import Task
from pawpal_system import Plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name_input = st.text_input("Owner name", value="Jordan")
owner_age_input = st.number_input("Owner age", min_value=0, max_value=120, value=30)
owner_gender_input = st.selectbox("Owner gender", ["male", "female", "other"], index=0)

# Persist owner in session state across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name_input,
        age=owner_age_input,
        gender=owner_gender_input,
    )

# Keep owner info constant once created; ignore input update after first set
owner = st.session_state.owner

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])    

# Persist pets in session state
if "pets" not in st.session_state:
    st.session_state.pets = []

if pet_name and species:
    if pet_name not in [p.name for p in st.session_state.pets]:
        # always keep owner consistent from st.session_state
        p = Pet(name=pet_name, species=species, breed="unknown", gender="unknown", weight=0.0, height=0.0, age=0, owner=owner)
        owner.add_pet(p)
        st.session_state.pets.append(p)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    start_time_text = st.text_input("Start time (HHMM)", value="0800")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    try:
        start_time_val = int(start_time_text) if start_time_text.strip() else None
    except ValueError:
        st.error("Start time must be a 24-hour number like 0800, 1330")
        start_time_val = None

    st.session_state.tasks.append(
        {
            "title": task_title,
            "start_time": start_time_val,
            "duration_minutes": int(duration),
            "priority": priority,
        }
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Build plan from current owner and tasks
    daily_plan = Plan(owner=owner)

    for task_data in st.session_state.tasks:
        # map priority text to numeric value
        priority_map = {"low": 1, "medium": 2, "high": 3}
        task_priority = priority_map.get(task_data.get("priority", "low"), 1)

        # resolve pet object
        task_pet = None
        if "pets" in st.session_state and task_data.get("pet"):
            task_pet = next((p for p in st.session_state.pets if p.name == task_data["pet"]), None)

        if task_pet is None and owner.pets:
            task_pet = owner.pets[0]

        if task_pet is None:
            continue

        task = Task(
            description=task_data.get("title", "Untitled"),
            start_time=task_data.get("start_time"),
            duration=task_data.get("duration_minutes", 1),
            location=task_data.get("location", "Unknown"),
            priority=task_priority,
            pets=[task_pet],
        )
        task_pet.add_task(task)
        daily_plan.add_task(task)

    st.warning(daily_plan.warning_message())
    st.markdown(daily_plan.schedule_markdown())

