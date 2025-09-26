from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired, ClientError
import time

def login_to_instagram(username, password):
    """
    Logs in to Instagram and returns the client object.
    Handles two-factor authentication (2FA) if required.
    """
    client = Client()
    try:
        client.login(username, password)
        print("Login successful!")
        return client
    except TwoFactorRequired:
        code = input("Two-factor authentication code required. Enter code: ")
        client.login(username, password, verification_code=code)
        print("Login successful with 2FA!")
        return client
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def fetch_and_like_posts(client, target_username, num_posts=5, delay=5):
    """
    Fetches the recent posts of the target user and likes them with a delay.
    """
    try:
        # Get the user ID of the target
        user_id = client.user_id_from_username(target_username)
        
        # Fetch the latest posts
        posts = client.user_medias(user_id, num_posts)
        
        if not posts:
            print(f"No posts found for user {target_username}.")
            return
        
        # Like each post with delay to avoid bot detection
        for post in posts:
            try:
                client.media_like(post.pk)
                print(f"Liked post ID: {post.pk}")
                time.sleep(delay)
            except ClientError as ce:
                print(f"Error liking post {post.pk}: {ce}")
                time.sleep(delay)
                
    except Exception as e:
        print(f"Error fetching or liking posts: {e}")

def main():
    """
    Main function to execute the bot.
    """
    # Replace with your Instagram credentials
    username = "your_username"
    password = "your_password"
    
    # Replace with the target username
    target_username = "target_user"
    
    # Number of posts to like
    num_posts = 5
    
    # Delay between likes (in seconds)
    delay = 5
    
    # Log in to Instagram
    client = login_to_instagram(username, password)
    
    if client:
        # Fetch and like posts
        fetch_and_like_posts(client, target_username, num_posts, delay)

if __name__ == "__main__":
    main()
