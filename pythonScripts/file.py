import requests


# api key and access token
with open("Api_key.txt", "r") as f:
    api_key = f.read().strip()

with open("Access_token.txt", "r") as f:
    access_token = f.read().strip()

# Reading the comments contained in msg.txt
with open("msg.txt", "r") as f:
    comment = f.read().strip()
# Reading the username from which the comment is being posted
with open("usr.txt", "r") as f:
    usernames = f.read().strip().split("\n")

endpoint_url = "https://api.truthsocial.com/v1/users/following"


payload = {
    "access_token": access_token,
    "api_key": api_key
}
response = requests.get(endpoint_url, params=payload)

if response.status_code == 200:
    followed_users = response.json()["data"]
    # Get recent posts from followed users
    for username in followed_users:
        user_posts_endpoint = f"https://api.truthsocial.com/v1/posts/user/{user['id']}/recent"
        user_posts_payload = {
            "access_token": access_token,
            "api_key": api_key
            }
        user_posts_response = requests.get(user_posts_endpoint, params=user_posts_payload)
        if user_posts_response.status_code == 200:
            user_posts = user_posts_response.json()
        # Posting the comments on most recent posts of the followed user
            for post in user_posts:
                for username in usernames:
                    payload = {
                        "username": username,
                        "message": comment,
                        "post_id": post["post_id"],
                        "access_token": access_token,
                        "api_key": api_key
                    }
                    response = requests.post("https://api.truthsocial.com/v1/posts/comment", data=payload)
                    if response.status_code == 200:
                        print(f"Comment posted on {username}'s post (ID: {post['post_id']}).")
                    else:
                        print(f"Failed to post comment on {username}'s post (ID: {post['post_id']}).")
            else:
                print(f"Failed to retrieve recent posts from user {user['username']}.")

else:
    print("Failed to retrieve followed users.")
