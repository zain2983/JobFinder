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
        time.sleep(4)  # Wait for the page to load


    try:
        # Wait for the parent element of the shadow root to be present
        parent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > faceplate-app > rs-app"))
        )

        # Access the shadow DOM and locate the textarea using JavaScript
        textarea = driver.execute_script("""
            let parent = document.querySelector("body > faceplate-app > rs-app").shadowRoot;
            let direct_chat = parent.querySelector("div.container > rs-direct-chat").shadowRoot;
            let composer = direct_chat.querySelector("section > rs-message-composer").shadowRoot;
            let textarea = composer.querySelector("form > div > rs-textarea-auto-size");
            return textarea.shadowRoot.querySelector("textarea");
        """)

        # Type a message into the located textarea
        textarea.send_keys("Hello, this is a test message!")

        print("Message successfully entered!")

    except Exception as e:
        print("Error accessing the shadow DOM or entering the message:", e)

        # Locate the input field using its class
        # input_field = driver.find_element(By.CSS_SELECTOR, "input.text-16.sm\\:text-14")  # Use escape for special characters
        # input_field = driver.find_element(By.CSS_SELECTOR, ".input-bar input")
        # input_field = driver.find_element(By.CSS_SELECTOR, ".input-bar input")
        # input_field = driver.find_element(By.CSS_SELECTOR, "div.input-bar input")
        # input_field = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-bar input"))
        # )
        # input_field = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-bar input"))
        # )


        # # Locate the message input field (modify selector if necessary)
        # message_field = driver.find_element(By.CSS_SELECTOR, ".DraftEditor-root")  # Update the selector if required

        # # Enter the message
        # message_field.send_keys(message_to_send)

        # # Press Enter to send the message
        # message_field.send_keys(Keys.RETURN)
        # time.sleep(2)  # Wait for the message to send

finally:
    # Close the browser
    driver.quit()



