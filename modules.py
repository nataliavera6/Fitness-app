#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################
import datetime
import streamlit as st
from internals import create_component


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Displays a user's post with their username, profile image, timestamp,
    content, and an optional post image.

    Args:
        username (str): The username of the user who made the post.
        user_image (str): The URL of the user's profile image.
        timestamp (str): The timestamp of the post.
        content (str): The content of the post.
        post_image (str): The URL of an image associated with the post (optional).
    """
    data = {
        'USERNAME': str(username),
        'PROFILE_IMAGE': user_image,
        'TIMESTAMP': str(timestamp),
        'CONTENT': str(content),
        'POST_IMAGE': post_image if post_image else "",
    }
    html_file_name = "my_custom_component"
    create_component(data, html_file_name, height=300)

    pass


# def display_activity_summary(workouts):
#     # Only show the general summary and exclude specific workouts
#     total_steps = sum(workout['TotalSteps'] for workout in workouts)
#     total_distance = sum(workout['TotalDistance'] for workout in workouts)
#     total_calories = sum(workout['CaloriesBurned'] for workout in workouts)
    
#     st.subheader("Activity Summary:")
#     st.write(f"Total Steps: {total_steps}")
#     st.write(f"Total Distance (mi): {total_distance:.2f}")
#     st.write(f"Total Calories Burned: {total_calories:.2f}")
#     pass

def display_activity_summary(workouts):
    if not workouts:
        create_component({"message": "No workouts yet."}, "display_activity_summary")
        return

    total_steps = 0
    total_distance = 0
    total_calories = 0
    total_time = datetime.timedelta()
    # Normalize keys to lowercase
    for workout in workouts:
        total_distance = total_distance + workout["TotalDistance"]
        total_steps = total_steps + workout["TotalSteps"]
        total_calories = total_calories + workout["CaloriesBurned"]
        start = datetime.datetime.strptime(str(workout['StartTimestamp']), "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(str(workout['EndTimestamp']), "%Y-%m-%d %H:%M:%S")
        if total_time == None:
            total_time = end-start
        else:
            total_time = total_time + (end-start)

    
    summary = {
        "TOTAL_STEPS": total_steps,
        "TOTAL_DISTANCE": total_distance,
         "TOTAL_EXCERISED": total_time,
        "TOTAL_CAL": total_calories
    }

    create_component(summary, "display_activity_summary")
def display_recent_workouts(workouts_list):
    """Function to display recent workouts."""
    data = []
    for workout in workouts_list:
        # Normalize keys
        w = {k.lower(): v for k, v in workout.items()}
        start_coords = w.get("start_lat_lng", ("?", "?"))
        end_coords = w.get("end_lat_lng", ("?", "?"))

        data.append({
            "Start Time": w.get("start_timestamp", "N/A"),
            "End Time": w.get("end_timestamp", "N/A"),
            "Distance (mi)": w.get("distance", "N/A"),
            "Steps": w.get("steps", "N/A"),
            "Calories Burned": w.get("calories_burned", "N/A"),
            "Start Coordinates": f"({start_coords[0]}, {start_coords[1]})",
            "End Coordinates": f"({end_coords[0]}, {end_coords[1]})"
        })

    create_component(data, "display_recent_workouts")

# def display_recent_workouts(workouts_list):
#     """Function to display recent workouts."""
#     data = []
#     for workout in workouts_list:
#         print(workout)
#         data ={
#             "Start Time": workout["StartTimestamp"],
#             "End Time": workout["EndTimestamp"],
#             "Distance (mi)": workout["TotalDistance"],
#             "Steps": workout["TotalSteps"],
#             "Calories Burned": workout["CaloriesBurned"],
#             "Start Coordinates": f"({workout['StartLocationLat']}, {workout['StartLocationLong']})",
#             "End Coordinates": f"({workout['EndLocationLat']}, {workout['EndLocationLong']})"
#         }
#     html_file_name = "display_recent_workouts"
#     create_component(data, html_file_name)
#     return data


    

def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'TIME': timestamp,
        'CONTENT': content,
        'IMAGE': image,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "display_genai_advice"
    create_component(data, html_file_name,height=160)

    
    pass

def display_sensors(userID, workout):
    """Displays sensor data for a user's workout."""
    st.markdown(f"### 🏃 FitRunner {userID[-3:].upper()}")  # Example display: FitRunner 007

    if not workout:
        st.write("No workout data available.")
        return

    # Display workout details if available
    st.write("Workout Details:")
    st.write(f"**Start Time:** {workout.get('StartTimestamp', 'N/A')}")
    st.write(f"**End Time:** {workout.get('EndTimestamp', 'N/A')}")
    st.write(f"**Distance (mi):** {workout.get('TotalDistance', 'N/A')}")
    st.write(f"**Steps:** {workout.get('TotalSteps', 'N/A')}")
    st.write(f"**Calories Burned:** {workout.get('CaloriesBurned', 'N/A')}")
    st.write(f"**Start Location:** ({workout.get('StartLocationLat', 'N/A')}, {workout.get('StartLocationLong', 'N/A')})")
    st.write(f"**End Location:** ({workout.get('EndLocationLat', 'N/A')}, {workout.get('EndLocationLong', 'N/A')})")

    