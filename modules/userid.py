import requests
from bs4 import BeautifulSoup
import json

def get_user_id(username):
    # Define the user's profile URL
    user_url = f"https://www.reddit.com/user/{username}/"

    # Send a GET request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the <reddit-page-data> tag
        element = soup.find("reddit-page-data")
        if element:
            data_attribute = element["data"]  # Extract the "data" attribute
            user_data = json.loads(data_attribute)  # Parse the JSON data

            # Extract the user ID
            user_id = user_data["profile"]["id"]
            return user_id
        else:
            print("reddit-page-data tag not found.")
            return None
    else:
        print(f"Failed to fetch page for {username}. Status code: {response.status_code}")
        return None
