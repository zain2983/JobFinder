import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from userid import get_user_id

# List of profile URLs
profile_urls = [
    "https://www.reddit.com/user/Comfortable-Draw4908/",
    # "https://www.reddit.com/user/wokenpoise8828/",
    # "https://www.reddit.com/user/AlexVonBronx/",
    # "https://www.reddit.com/user/Impressive-School-39/"
]


# Function to extract usernames from URLs
def extract_usernames(urls):
    usernames = [re.search(r'/user/([^/]+)/', url).group(1) for url in urls]
    return usernames

# Extracted usernames
usernames = extract_usernames(profile_urls)

user_ids = []

# Loop through each username and get their user ID
for username in usernames:
    user_id = get_user_id(username)  # Get the user ID using the function from reddit_scraper.py
    if user_id:
        user_ids.append(user_id)  # Append user ID to the list if it's valid
    else:
        print(f"User ID not found for username: {username}")

print("Username : " , username)
print("User ID : " , user_id)
# print(usernames)

# Message to send
message_to_send = "Hello! This is a test message."

# Set up Selenium WebDriver (ensure chromedriver is installed)
options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but useful in headless mode)
options.add_argument("--no-sandbox")  # Recommended for headless mode in some environments
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")


options.add_argument("user-data-dir=~/.config/google-chrome/Default")  # For Chrome

driver = webdriver.Chrome(options=options)


for i in user_ids:
    print("USER IDS : ------ ",i)

try:
    # Iterate over each username
    for user_id in user_ids:
        # Navigate to the chat page
        rrr = f"https://chat.reddit.com/user/id/{user_id}"
        print("Link : " ,rrr)
        driver.get(rrr)
        time.sleep(2)  # Wait for the page to load



    try:
        # Execute JavaScript to access the textarea inside the shadow DOM
        textarea_element = driver.execute_script("""
            return document.querySelector("body > faceplate-app > rs-app").shadowRoot
                .querySelector("div.container > rs-room-overlay-manager > rs-room").shadowRoot
                .querySelector("main > rs-message-composer").shadowRoot
                .querySelector("form > div > rs-textarea-auto-size textarea");
        """)

        # Interact with the located textarea
        if textarea_element:
            textarea_element.click()  # Focus the textarea
            textarea_element.send_keys("Hello, this is a test message!")  # Send the message
            textarea_element.send_keys(Keys.RETURN)
            time.sleep(4)
            print("Successfully interacted with the textarea!")
        else:
            print("Textarea element not found.")
    except Exception as e:
        print("Error accessing the textarea:", e)



finally:
    # Close the browser
    driver.quit()