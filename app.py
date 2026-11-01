from datetime import date

import streamlit as st

from pawpal_system import FREQUENCIES, PRIORITIES, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("Plan care tasks for your pets: feeding, walks, medication, and appointments.")
st.caption("Data lives in this browser session only; refreshing or restarting the app clears it.")

# Streamlit reruns this whole script on every click, so the owner is created once
# and kept in session_state; later reruns reuse the same object.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)

owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        else:
            try:
                owner.add_pet(Pet(pet_name.strip(), species))
                st.success(f"Added {pet_name.strip()} the {species}.")
            except ValueError as error:
                st.error(str(error))

st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task", clear_on_submit=True):
        chosen_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
        description = st.text_input("Task", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input("Date", value=date.today())
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            frequency = st.selectbox("Repeats", FREQUENCIES)
        with col2:
            task_time = st.time_input("Time (24-hour)", step=300)
            priority = st.selectbox("Priority", PRIORITIES, index=2)
        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == chosen_name)
            try:
                pet.add_task(
                    Task(
                        description.strip() or "Task",
                        due_date,
                        task_time.strftime("%H:%M"),
                        int(duration),
                        priority,
                        frequency,
                    )
                )
                st.success(f"Scheduled '{description}' for {pet.name} at {task_time:%H:%M}.")
            except ValueError as error:
                st.error(str(error))

st.divider()

st.subheader(f"Today's Schedule ({date.today():%A, %B %d})")

# A Done click reruns the script after the table above it was drawn, so the result
# message is saved here and shown after st.rerun() redraws everything.
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

conflicts = scheduler.find_conflicts()
for warning in conflicts:
    st.warning(f"⚠️ {warning}")
if not conflicts:
    st.success("No scheduling conflicts.")

todays = scheduler.sort_by_time(scheduler.todays_tasks())
if not todays:
    st.info("Nothing scheduled for today.")
for pet, task in todays:
    info, action = st.columns([5, 1])
    status = "✅ done" if task.completed else f"{task.priority} priority"
    info.markdown(
        f"**{task.time}** · {pet.name} · {task.description} "
        f"({task.duration_minutes} min, {status})"
    )
    if not task.completed and action.button("Done", key=f"done-{id(task)}"):
        next_task = scheduler.complete_task(pet, task)
        message = f"{task.description} for {pet.name} is done."
        if next_task is not None:
            message += f" Next one is due {next_task.due_date:%a %b %d} at {next_task.time}."
        st.session_state.flash = message
        st.rerun()

st.subheader("All Tasks")
if not owner.pets:
    st.info("No pets yet.")
else:
    col1, col2 = st.columns(2)
    with col1:
        pet_choice = st.selectbox("Pet", ["All pets"] + [pet.name for pet in owner.pets], key="filter_pet")
    with col2:
        status_choice = st.radio("Status", ["All", "Incomplete", "Completed"], horizontal=True)
    completed_filter = {"All": None, "Incomplete": False, "Completed": True}[status_choice]
    pet_filter = None if pet_choice == "All pets" else pet_choice

    matches = scheduler.sort_by_time(scheduler.filter_tasks(pet_name=pet_filter, completed=completed_filter))
    if matches:
        st.table(
            [
                {
                    "Date": task.due_date.isoformat(),
                    "Time": task.time,
                    "Pet": pet.name,
                    "Task": task.description,
                    "Minutes": task.duration_minutes,
                    "Priority": task.priority,
                    "Repeats": task.frequency,
                    "Done": "yes" if task.completed else "no",
                }
                for pet, task in matches
            ]
        )
    else:
        st.info("No tasks match these filters.")
