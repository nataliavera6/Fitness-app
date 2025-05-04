import os
from google.cloud import bigquery



def get_client():
    return bigquery.Client()

def get_users():
    client = get_client()
    # Correct table_id format
    friends_table = 'kappletechx25-448818.ISE.Friends'

    users_table = 'kappletechx25-448818.ISE.Users'

    # Query setup
    friends_query = f'SELECT * FROM `{friends_table}` LIMIT 10'

    users_query = f'SELECT * FROM `{users_table}` LIMIT 10'

    # Run the query
    friend_query_job = client.query(friends_query)

    users_query_job = client.query(users_query)

    # Wait for the query to finish and get the result
    friends_results = friend_query_job.result()

    users_results = users_query_job.result()


    users = {}

    # Process the user results to build the users dictionary
    for row in users_results:
        user_id, full_name, username, profile_image, date_of_birth = row
        users[user_id] = {
            'full_name': full_name,
            'username': username,
            'date_of_birth': str(date_of_birth),
            'profile_image': profile_image,
            'friends': [],# We'll populate this later
        }

    # Process the friends results to populate the friends list
    for row in friends_results:
        user1, user2 = row
        if user1 in users:
            users[user1]['friends'].append(user2)
        if user2 in users:
            users[user2]['friends'].append(user1)    
    # The final dictionary `users` will now contain all the user information with their friends populated
    # print(users)
    return users


def get_post_table(user_id):
    client = get_client()
    posts_table = 'kappletechx25-448818.ISE.Posts'
    posts_query = f'SELECT * FROM `{posts_table}` LIMIT 10'
    posts_query_job = client.query(posts_query)
    posts_results = posts_query_job.result()
    posts={}
    for row in posts_results:
        PostId, AuthorId, Timestamp, ImageUrl, Content = row
        posts[AuthorId]={
            'postId':PostId,
            'authorId':AuthorId,
            'Timestamp':Timestamp,
            'ImageUrl':ImageUrl,
            'content':Content    
        }
    return posts

