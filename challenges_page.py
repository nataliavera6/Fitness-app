import streamlit as st
from data_fetcher import get_challenges



def display_challenges():
    st.title("🏆 Challenges")
    st.write("Track your weekly progress and view all current challenges.")
    challenges=[]
    challenge_dict= get_challenges()
    # Define the challenges
    if not challenge_dict or len(challenge_dict) == 0:
        challenges = [
            {
                "title": "Walk for 3 minutes",
                "description": "Go for a 30 minute walk at any pace.",
                "details": ["Walk outside or on a treadmill", "Track your time with any fitness app"]
            },
            {
                "title": "Drink 8 Glasses of Water",
                "description": "Stay hydrated throughout the day.",
                "details": ["8 glasses = ~64 oz or ~2 liters", "Use a water tracker app if needed"]
            },
            {
                "title": "Climb 100 Stairs",
                "description": "Accumulate a total of 100 steps climbed.",
                "details": ["Find a set of stairs to use", "Climb up and down the stairs", "Repeat until you have reached 100 stairs total"]
            },
            {
                "title": "Try a Yoga Stretch",
                "description": "Try a yoga stretch or pose.",
                "details": ["Find a quiet place to stretch", "Follow a yoga video or guide", "Hold the pose for 20-30 seconds"]
            }
        ]
    else:

        for title, steps in challenge_dict.items():

            challenges.append({
                "title": title,
                "description": steps[2],
                "details": steps[3:]
            })


    # Loop through each challenge to display it
    for i, challenge in enumerate(challenges):
        with st.container():
            st.subheader(challenge["title"])
            st.write(challenge["description"])

            # Generate unique keys for each button and expander
            button_key = f"view_details_{i}"
            complete_button_key = f"complete_{i}"

            # Check if this challenge's details have been expanded in session state
            if f"expanded_{i}" not in st.session_state:
                st.session_state[f"expanded_{i}"] = False

            # Button to view details
            # if st.button("View Details", key=button_key):
            #     # Toggle expanded state for this challenge
            #     st.session_state[f"expanded_{i}"] = not st.session_state[f"expanded_{i}"]

            # # Show the details based on the expanded state
            # if st.session_state[f"expanded_{i}"]:
            with st.expander("Challenge Details"):
                
                for detail in range(len(challenge["details"]) - 1):
                    if detail % 2 == 0:
                        st.write(f"{challenge['details'][detail]} {challenge['details'][detail+1]}")
                    
                if st.button("Mark as Complete", key=complete_button_key):
                    st.success(f"🎉 YOUVE COMPLETED '{challenge['title']}'!")

# Displaying the challenges on your app
if __name__ == "__main__":
    display_challenges()
