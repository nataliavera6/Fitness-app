import streamlit as st
from datetime import datetime, date, timedelta
import os
# Assuming setup_database.py has populated the 'users' dictionary
try:
    from setup_database import users
except :
    from data_fetcher import users
    # users = {}
    # st.error("Error: setup_database.py not found or did not correctly populate the 'users' dictionary. Habit tracking will be limited.")

# --- Habit Data Structure (In-memory for simplicity with provided files) ---
# In a real application, this would likely be a database.
user_habits_data = {}  # {user_id: [{'habit_id': 1, 'name': '...', ... , 'completions': ['2025-04-21', ...]}]}
next_habit_id = 1

def initialize_habits(user_id):
    if user_id not in user_habits_data:
        user_habits_data[user_id] = []

def _get_habit_by_id(user_id, habit_id):
    initialize_habits(user_id)
    for habit in user_habits_data[user_id]:
        if habit['habit_id'] == habit_id:
            return habit
    return None

# Add a new habit for a user
def add_habit(user_id, name, description, frequency):
    global next_habit_id
    initialize_habits(user_id)
    if any(habit['name'] == name for habit in user_habits_data[user_id]):
        st.error(f"Habit '{name}' already exists.")
        return False
    start_date = date.today().strftime('%Y-%m-%d')
    new_habit = {
        'habit_id': next_habit_id,
        'name': name,
        'description': description,
        'frequency': frequency,
        'start_date': start_date,
        'completions': []
    }
    user_habits_data[user_id].append(new_habit)
    next_habit_id += 1
    return True

# Edit an existing habit
def edit_habit(user_id, habit_id, name, description, frequency):
    habit = _get_habit_by_id(user_id, habit_id)
    if not habit:
        st.error(f"Habit with ID {habit_id} not found.")
        return False
    if any(h['name'] == name and h['habit_id'] != habit_id for h in user_habits_data[user_id]):
        st.error(f"Habit '{name}' already exists.")
        return False
    habit['name'] = name
    habit['description'] = description
    habit['frequency'] = frequency
    return True

# Delete a habit
def delete_habit(user_id, habit_id):
    initialize_habits(user_id)
    habit_to_delete = _get_habit_by_id(user_id, habit_id)
    if habit_to_delete:
        user_habits_data[user_id].remove(habit_to_delete)
        return True
    st.error(f"Habit with ID {habit_id} not found.")
    return False

# Get all habits for a specific user
def get_habits(user_id):
    initialize_habits(user_id)
    return user_habits_data.get(user_id, [])

# Record the completion of a habit for a specific date
def complete_habit(user_id, habit_id, completion_date_str):
    habit = _get_habit_by_id(user_id, habit_id)
    if not habit:
        st.error(f"Habit with ID {habit_id} not found.")
        return False
    if completion_date_str not in habit['completions']:
        habit['completions'].append(completion_date_str)
        return True
    st.info(f"Habit already marked as completed on {completion_date_str}.")
    return False

# Get the completion status of a habit for a given date
def is_habit_completed(user_id, habit_id, check_date_str):
    habit = _get_habit_by_id(user_id, habit_id)
    if habit:
        return check_date_str in habit['completions']
    return False

# Get the completion dates for a specific habit
def get_habit_completions(user_id, habit_id):
    habit = _get_habit_by_id(user_id, habit_id)
    if habit:
        return sorted(habit['completions'], reverse=True)
    return []

# Calculate the current streak for a habit
def get_current_streak(user_id, habit_id):
    completions = get_habit_completions(user_id, habit_id)
    if not completions:
        return 0

    today = date.today()
    streak = 0
    current_date = today

    while True:
        check_date_str = current_date.strftime('%Y-%m-%d')
        if check_date_str in completions:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    return streak

# Calculate the longest streak for a habit
def get_longest_streak(user_id, habit_id):
    completions = sorted([datetime.strptime(d, '%Y-%m-%d').date() for d in get_habit_completions(user_id, habit_id)])
    if not completions:
        return 0

    longest_streak = 0
    current_streak = 0
    i = 0
    while i < len(completions):
        current_streak = 1
        j = i + 1
        while j < len(completions) and (completions[j] - completions[j-1]) == timedelta(days=1):
            current_streak += 1
            j += 1
        longest_streak = max(longest_streak, current_streak)
        i = j

    return longest_streak
# ✅ This is the function to import and use in app.py
def display_habit_tracker():
    st.title("🧭 Habit Tracker")
    user_id = "user1"

    st.subheader("Your Habits")
    habits = get_habits(user_id)

    if not habits:
        st.info("No habits yet. Add one below!")
    else:
        for habit in habits:
            st.markdown(f"### {habit['name']}")
            st.write(f"- **Description**: {habit['description']}")
            st.write(f"- **Frequency**: {habit['frequency']}")
            st.write(f"- **Completions**: {', '.join(get_habit_completions(user_id, habit['habit_id']))}")
            st.write(f"- **Current Streak**: {get_current_streak(user_id, habit['habit_id'])}")
            st.write(f"- **Longest Streak**: {get_longest_streak(user_id, habit['habit_id'])}")

    st.subheader("Add a New Habit: ")
    with st.form("add_habit_form"):
        name = st.text_input("Habit Name")
        description = st.text_input("Description")
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
        submit = st.form_submit_button("➕Add Habit")
        if submit:
            added = add_habit(user_id, name, description, frequency)
            if added:
                st.success(f"Habit '{name}' added!")

    st.subheader("💧 Water and Sleep Tracker")

    html_path = os.path.join(os.path.dirname(__file__), "custom_components/habit_tracker.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    st.components.v1.html(html_code, height=1100, scrolling=True)
# if __name__ == "__main__":
#     user_id = "user1"  # Assuming a user ID from your 'users' dictionary

#     # Example Usage
#     if user_id in users:
#         print(f"Habit Tracker for user: {users[user_id].get('username', user_id)}")

#         # Add some habits
#         add_habit(user_id, "Drink Water", "Drink 8 glasses", "daily")
#         add_habit(user_id, "Code for 1 hour", "Work on a project", "daily")
#         add_habit(user_id, "Read News", "Stay informed", "daily")

#         # Complete some habits
#         today = date.today()
#         yesterday = today - timedelta(days=1)
#         two_days_ago = today - timedelta(days=2)

#         habits = get_habits(user_id)
#         for habit in habits:
#             if habit['name'] == "Drink Water":
#                 complete_habit(user_id, habit['habit_id'], today.strftime('%Y-%m-%d'))
#                 complete_habit(user_id, habit['habit_id'], yesterday.strftime('%Y-%m-%d'))
#             if habit['name'] == "Code for 1 hour":
#                 complete_habit(user_id, habit['habit_id'], today.strftime('%Y-%m-%d'))
#             if habit['name'] == "Read News":
#                 complete_habit(user_id, habit['habit_id'], yesterday.strftime('%Y-%m-%d'))
#                 complete_habit(user_id, habit['habit_id'], two_days_ago.strftime('%Y-%m-%d'))

#         # Display habits and stats
#         user_habits = get_habits(user_id)
#         print("\nYour Habits:")
#         for habit in user_habits:
#             print(f"  - Name: {habit['name']}")
#             print(f"    Description: {habit['description']}")
#             print(f"    Frequency: {habit['frequency']}")
#             print(f"    Start Date: {habit['start_date']}")
#             print(f"    Completions: {get_habit_completions(user_id, habit['habit_id'])}")
#             print(f"    Current Streak: {get_current_streak(user_id, habit['habit_id'])}")
#             print(f"    Longest Streak: {get_longest_streak(user_id, habit['habit_id'])}")
#             print("-" * 20)

#         # Example of checking completion
#         drink_water_habit = next((h for h in user_habits if h['name'] == "Drink Water"), None)
#         if drink_water_habit:
#             print(f"\nDid you drink water today ({today.strftime('%Y-%m-%d')})? {is_habit_completed(user_id, drink_water_habit['habit_id'], today.strftime('%Y-%m-%d'))}")
#             print(f"Did you drink water yesterday ({yesterday.strftime('%Y-%m-%d')})? {is_habit_completed(user_id, drink_water_habit['habit_id'], yesterday.strftime('%Y-%m-%d'))}")
#     else:
#         print(f"User with ID '{user_id}' not found in setup_database.py")