#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################
import random
import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
# from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, get_user_previous_day
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts,users

from navigation_bar import navigation
from community_page import render_community_page
from activity_page import activity_page
from challenges_page import display_challenges
from habit_tracker import display_habit_tracker
userId = 'user1'

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "show_popup" not in st.session_state:
    st.session_state.show_popup = True

# ---- Display Navigation Bar ----
navigation()

def weekly_challenge_popup():
    if st.session_state.show_popup and st.session_state.page == "Activity":
        with st.container():
            st.markdown("### 💪 Weekly Challenge!")
            st.info("Complete 5 workouts this week to earn a badge!")
            if st.button("Got it!"):
                st.session_state.show_popup = False

# ---- Page Functions ----
def display_home():
    st.title('🏃 FitRunner 007')
    weekly_challenge_popup()

    # Check if the post has already been displayed
    if 'post_displayed' not in st.session_state:
        st.session_state.post_displayed = True
        # Display the post only once
        user_data = get_user_posts(userId)[0]
        display_post(user_data['user_id'], user_data['image'], user_data['timestamp'], user_data['content'], None)

    # Display GenAI advice and activity summary
    advice = get_genai_advice(users, userId)
    display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
    #display_activity_summary(get_user_workouts(userId))



def display_profile():
    st.title("👤 Profile")
    st.write("View and edit your fitness profile.")

def display_home_page():
    st.title("🏃 Welcome to FitRunner 007!")
    st.write("This is your fitness dashboard. ")
    st.write("Explore the app, track your progress, and complete challenges!")

def display_habit_tracker_page():
    st.title("Habit Tracker")




# ---- Page Routing ----
if st.session_state.page == "Home":
    display_home()
elif st.session_state.page == "Community":
    render_community_page(userId)  
elif st.session_state.page == "Activity":
    activity_page(userId) 
elif st.session_state.page == "Challenges":
    display_challenges() 
elif st.session_state.page == "Habit Tracker":

    display_habit_tracker() 

