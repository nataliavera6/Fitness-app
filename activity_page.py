import streamlit as st
import sqlite3
from datetime import datetime
from data_fetcher import get_user_sensor_data, get_user_workouts
from google.cloud import bigquery
client = bigquery.Client()
project_database = "kappletechx25-448818.ISE."

def get_activity_summary(user_id):
    all_activity = get_user_workouts(user_id)
    total_workouts = len(all_activity)
    Total_Distance = 0
    Total_Steps = 0
    Total_Calories = 0
    for i in all_activity:
        Total_Distance += i["TotalDistance"]
        Total_Steps += i["TotalSteps"]
        Total_Calories += i["CaloriesBurned"]
    return [total_workouts, Total_Steps/total_workouts, Total_Calories/total_workouts]

 
def create_post(user_id, content):
    try:
        query = f"SELECT COUNT(*) FROM `{project_database}Posts`"  # Added backticks
        tmp = client.query(query)
        results = list(tmp)
        num = 0
        for row in results:
            num = row[0]
        
        rows_to_insert = [
            {"PostId": f"post{num+1}", "AuthorId": user_id, "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "ImageUrl": "", "content": content}
        ]
        table_id = f"{project_database}Posts"
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if errors == []:
            print("Post created successfully!")
            return True
        else:
            print(f"errors during insert {errors}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

# Activity Page
def activity_page(user_id):
    if "shared" not in st.session_state:
        st.session_state["shared"] = False

    st.title("Activity Dashboard")
    
        
   
    
    workouts = get_user_workouts(user_id)
    summary = get_activity_summary(user_id)

    # Recent workouts
    st.header("Recent Workouts")
    if workouts:
        for workout in workouts:
            with st.expander(f"Workout on {workout['StartTimestamp']}"):
                st.write(f"Workout ID: {workout['WorkoutId']}")
                st.write(f"Start Time: {workout['StartTimestamp']}")
                st.write(f"End Time: {workout['EndTimestamp']}")
                st.write(f"Distance: {workout['TotalDistance']} km")
                st.write(f"Steps: {workout['TotalSteps']}")
                st.write(f"Calories Burned: {workout['CaloriesBurned']} kcal")
                st.write("")
                st.write("Sensor Data")
                sensor = get_user_sensor_data(user_id, workout["WorkoutId"])
                heartbeat = None
                steps = None
                temp = None
                for i in sensor:
                    if i["Name"] == "Temperature":
                        temp = i["SensorValue"]
                    if i["Name"] == "Heart Rate":
                        heartbeat = i["SensorValue"]
                    if i["Name"] == "Step Count":
                        steps = i["SensorValue"]

                st.write(f"Heartbeat: {heartbeat}")
                st.write(f"Steps: {steps}")
                st.write(f"Temperature: {temp}")
    else:
        st.info("No workouts found.")

    # Activity Summary
    st.header("Activity Summary")
    st.metric("Total Workouts", summary[0])
    st.metric("Total Steps", f"{summary[1],}")
    st.metric("Total Calories", f"{summary[2],} kcal")

    # Share button
    st.header("Share Your Progress")
    share_option = st.radio("Choose what to share:", ["Steps from latest workout", "Total steps", "Total calories burned"])
    
    if share_option == "Steps from latest workout" and workouts:
        message = f"Look at this, I walked {workouts[0]['TotalSteps']:,} steps today!"
    elif share_option == "Total steps":
        message = f"I've walked {summary[1]:,} steps in total!"
    else:
        message = f"I've burned {summary[2]:,} calories so far!"

    if st.button("Share!"):
        create_post(user_id, message)
        st.success("✅ Your post has been shared!")
        st.markdown(f"**📢 {message}**")

# Example usage
if __name__ == "__main__":
    user_id = "user1"
    activity_page(user_id)
