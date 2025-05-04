#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import random
import sqlite3
from google.cloud import bigquery

from datetime import datetime

import os
from setup_database import get_users,get_post_table
import vertexai
from vertexai.generative_models import GenerativeModel

from dotenv import load_dotenv
import re

from google.cloud import bigquery
from vertexai.preview.generative_models import GenerativeModel

import json, os, re

from dotenv import load_dotenv

import pickle

#BigQuery Client
client = bigquery.Client()
project_database = "kappletechx25-448818.ISE."




users=get_users()
# users = {
#     'user1': {
#         'full_name': 'Remi',
#         'username': 'remi_the_rems',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user2', 'user3', 'user4'],
#     },
#     'user2': {
#         'full_name': 'Blake',
#         'username': 'blake',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1'],
#     },
#     'user3': {
#         'full_name': 'Jordan',
#         'username': 'jordanjordanjordan',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1', 'user4'],
#     },
#     'user4': {
#         'full_name': 'Gemmy',
#         'username': 'gems',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1', 'user3'],
#     },
# }


def get_user_sensor_data(user_id, workout_id):
    """Returns a list of timestampped information for a given workout.
    """

    try:
        query = f"SELECT * FROM `{project_database}SensorData` WHERE WorkoutID = '{workout_id}'"
        tmp = None
        list_of_sensors = []
        tmp = client.query(query)
        results = list(tmp) #convert query results to a list.
        for row in results:
            dictonary = dict(row)
            list_of_sensors.append(dictonary)
        sensor_data = list_of_sensors

        for data in sensor_data:
             query = f"SELECT * FROM `{project_database}SensorTypes` WHERE SensorId = '{data['SensorId']}'"
             tmp = client.query(query)
             results = list(tmp)
             first_row = dict(results[0])
             data["Name"] = first_row['Name']
             data["Units"] = first_row["Units"]
         
        return sensor_data
    except Exception as E:
        return None


def get_user_workouts(user_id):
    workouts = []
    # Check if user exists
    query = f"SELECT * FROM `{project_database}Workouts` WHERE UserId = '{user_id}'"
    tmp = client.query(query)        
    results = list(tmp)
    for row in results:
        dictonary = dict(row)
        workouts.append(dictonary)
    return workouts
        

def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')
    

    return users[user_id]


def get_user_posts(user_id):
    """Returns a list of a user's posts.

    This function currently returns random data. You will re-write it in Unit 3.
    """

    posts=get_post_table(user_id)
    # content = random.choice([
    #     'Had a great workout today!',
    #     'The AI really motivated me to push myself further, I ran 10 miles!',
    # ])

    return [{
        'user_id': posts[user_id]['authorId'],
        'post_id':posts[user_id]['postId'],
        'timestamp': posts[user_id]['Timestamp'],
        'content': posts[user_id]['content'],
        'image': posts[user_id]['content'],
    }]

def get_response(users, user_id):
    # TODO: Rename ".env.template" to ".env" and add your project ID to it.
    from dotenv import load_dotenv

    load_dotenv()

    vertexai.init(project=os.environ.get("kappletechx25-448818"), location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    response = model.generate_content(
        f"Give me good one sentence inspirational advice for {users[user_id]['username']}'s workout "
    )

    return response


def get_genai_advice(users, user_id):
    """
    Returns the most recent advice from the genai model for a given user.
    """
    response = get_response(users, user_id)

    # Extract the content from the response
    if not response.candidates:
        content = ""
    else:
        try:
            content = response.candidates[0].content.parts[0].text
        except (AttributeError, IndexError):
            content = "There was an error processing the advice."

    # Choose randomly whether to include an image
    image_url = 'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    include_image = random.choice([True, False])
    image = image_url if include_image else None

    # Get current time
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'advice_id': 'advice1',
        'timestamp': current_timestamp,
        'content': content,
        'image': image,
    }



def get_challenges():
    
    # Path to store challenge data
    CHALLENGE_CACHE = "weekly_challenge.pkl"

    # Check if today is Monday
    today = datetime.now().strftime("%A")
    is_monday = today == "Monday"

    # If it's not Monday, load the last saved challenge_dict
    if not is_monday and os.path.exists(CHALLENGE_CACHE):
        with open(CHALLENGE_CACHE, "rb") as f:
            challenge_dict = pickle.load(f)
        if len(challenge_dict)>1:
            print("Loaded previous challenge (not Monday)")
            return challenge_dict

    # Otherwise, generate new challenges
    load_dotenv()
    vertexai.init(project=os.environ.get("PROJECT_ID"), location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content("Give me 3 daily workout challenges with a title and description to complete")

    text = response.text if hasattr(response, "text") else response.parts[0].text
    print(text)
    lines = text.strip().split("\n")
    content = "\n".join(lines[1:])  # Remove the first line

    raw_challenges = re.split(r'\*\*\d+\.\s*Title:', content)

    challenge_dict = {}

    for chunk in raw_challenges:
        chunk = chunk.strip()
        if not chunk:
            continue

        match = re.match(r'\s*The\s+"[^"]+"', chunk)
        if match:
            title = match.group(0).strip()
            body = chunk.replace(title, "").strip()
            parts = [section.strip() for section in re.split(r'\*|\n', body) if section.strip()]
            challenge_dict[title] = parts

    # Save the new challenge dictionary
    with open(CHALLENGE_CACHE, "wb") as f:
        pickle.dump(challenge_dict, f)
    print("New challenge generated and saved (Monday)")
    

    return challenge_dict


#use this to view challenges
# challenge_dict= get_challenges()
# print(challenge_dict)
# for title, steps in challenge_dict.items():
#     print(" ")
#     print("NEXT CHALLENGE")
#     print(steps)
#     for step in steps:
#         print(step)


