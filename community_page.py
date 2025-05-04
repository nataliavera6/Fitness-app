import random
from datetime import datetime
import streamlit as st
# Assuming the following functions are imported from your data_fetcher.py
from data_fetcher import get_user_posts, get_genai_advice, users
from modules import display_genai_advice, display_post  # assuming these are imported

userId='user1'


def render_community_page(user_id):
    """Render the community home page with friends' posts and GenAI advice."""
    # Get the posts from the user's friends
    posts=[]
    st.title(f"Welcome back {users[user_id]['username']}!")
    # st.title(f"Welcome back {users[userId]['username']}!")

    for friendUserId in users[userId]['friends']:
        for post in get_user_posts(friendUserId):

            posts.append(post)
 

    # Sort posts by timestamp in descending order (latest posts first)
    posts_sorted = sorted(posts, key=lambda x: x['timestamp'], reverse=True)


    
    
    print(f"\nRecent Posts from {user_id}'s Friends:")

    # Display the first 10 posts
    for i in range(min(10, len(posts_sorted))):
        username = users[posts_sorted[i]['user_id']]['username']
        timestamp = posts_sorted[i]['timestamp']
        profile_image = posts_sorted[i]['image']
        content = posts_sorted[i]['content']
        display_post(username, profile_image, timestamp, content, None)


# Get one piece of GenAI advice and encouragement
genai_advice = get_genai_advice(users, userId)
# Display the GenAI advice
display_genai_advice(
    timestamp=genai_advice['timestamp'], 
    content=genai_advice['content'], 
    image=genai_advice['image']
)
render_community_page(userId)



