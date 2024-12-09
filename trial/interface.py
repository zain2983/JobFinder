# importing all libraries
import streamlit as st
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from groq import Groq
import requests
from bs4 import BeautifulSoup
import json
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
from datetime import datetime
import sys




def scrape(url_list,total_posts=3):

    # List of URLs to scrape
    # urls = [
    #     "https://www.reddit.com/r/slavelabour/new/",
    #     # "https://www.reddit.com/r/forhire/new/",
    #     # "https://www.reddit.com/r/VideoEditor_forhire/new/",
    #     # "https://www.reddit.com/r/DoneDirtCheap/new/",
    #     # "https://www.reddit.com/r/freelance_forhire/new/",
    #     # "https://www.reddit.com/r/FreelanceProgramming/new/",
    #     # "https://www.reddit.com/r/HireAnEditor/new/",
    # ]
    urls = url_list

    print("starting to setup webdriver")
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but useful in headless mode)
    options.add_argument("--no-sandbox")  # Recommended for headless mode in some environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print('Completed settings for webdriver\nNow starting to tscrape data')
    scraped_data = []

    i=0

    for url in urls:

    # Scraping the Jobs

        driver.get(url)
        time.sleep(1)
        print(f"Scraping ----- {url}...")

        # Accept Reddit's cookies if prompted (optional)
        try:
            cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
            cookies_button.click()
        except:
            pass

        # Scroll the page a few times to load more posts
        scroll_pause_time = 2
        scroll_count = 4

        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # After scrolling, get the page source for Beautiful Soup
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all post containers
        posts = soup.find_all(id=lambda x: x and x.startswith("post-title-t3_"))

      
        # Loop through each post container and extract data



        for post in posts[:25]:
            post_id = post.get("id").replace("post-title-", "")
            title = post.get_text(strip=True)
            print(url," ===== " , i)
            link_tag = post.find_previous("a", href=True)
            user_id_link = link_tag['href'] if link_tag else "N/A"
            if user_id_link != "N/A" and not user_id_link.startswith("http"):
                user_id_link = "https://www.reddit.com" + user_id_link

            description_div = soup.find(id=f"{post_id}-post-rtjson-content")
            if description_div:
                paragraphs = description_div.find_all("p")
                description = "\n".join([p.get_text(strip=True) for p in paragraphs])
            else:
                description = "N/A"


            modified_url = url.replace("new/", f"comments/{post_id}/")
            # print(modified_url)

            post_data = {
                "Post ID": post_id,
                "UserID Link": user_id_link,
                "Post Link": modified_url, 
                "Title": title,
                "Flair": 'N/A Flair Text - Manually Added',
                "Description": description
            }
            scraped_data.append(post_data)
            i+=1

    print("Total Scraped : " , i )
    driver.quit()
    return scraped_data





def classify(scraped_data, keywords):
    # Create a regular expression pattern from the keywords list
    keywords_pattern = r"|".join(map(re.escape, keywords))

    for i in scraped_data:
        title = i.get('Title', '')
        description = i.get('Description', '')
        tags = "Other"

        # Check if any keyword exists in the title or description
        if re.search(keywords_pattern, title, re.IGNORECASE) or re.search(keywords_pattern, description, re.IGNORECASE):
            tags = "yes"

        i['Tags'] = [tags]
    
    return scraped_data






# Set up Streamlit app
st.title("Reddit Messenger")

# Input for subreddits
subreddits_input = st.text_input("Subreddits", placeholder="Enter the links of the subreddits that you wanna scrape - seperated by comma")

# Input for keywords
keyword = st.text_input("Keywords", placeholder="Enter the keywords to search for")

# Button to trigger scraping
if st.button("Scrape"):
    if subreddits_input and keyword:
        with st.spinner("Getting posts"):
            subreddits = [sub.strip() for sub in subreddits_input.split(",") if sub.strip()]

            # subreddits = [url if url.endswith("/") else url + "/" for url in subreddits]

            formatted_subreddits = []

            for item in subreddits:
                if item.startswith("http"):  # Check if the input is a URL
                    # Ensure the URL ends with a "/"
                    formatted_url = item if item.endswith("/") else item + "/"
                else:
                    # Construct the URL from the subreddit name
                    formatted_url = f"https://www.reddit.com/r/{item}/"
                
                formatted_subreddits.append(formatted_url)

            subreddits = formatted_subreddits
            subreddits = [sub + "new/" for sub in subreddits]
            
            for i in subreddits:
                print(i)


            keywords = [sub.strip() for sub in keyword.split(",") if sub.strip()]
            print("Keywords : " , keywords)

            # scraped_posts = scrape(url_list=subreddits)
            # data_w_tags = classify(scraped_data=scraped_posts,keywords=keywords)
            scraped_posts = []
            data_w_tags = []
        
        # scraped_posts = [  # Replace with actual scraped data
        #     f"Post {i}: A post about {keywords} in subreddit {subreddits}" 
        #     for i in range(1, 6)
        # ]
        st.write("Total posts found : " , len(scraped_posts))

        filtered_posts = [post for post in scraped_posts if "yes" in post.get("Tags", [])]

        st.write("Total Posts that contain the keywords : " , len(filtered_posts))

        with st.container(height=350,border=True):
            st.subheader("Filtered Posts with 'yes' Tags")
            if filtered_posts:
                for post in filtered_posts:
                    st.write(f"**Post Link**: {post["Post Link"]}")
                    st.write(f"**Title**: {post['Title']}")
                    st.write(f"**Description**: {post['Description']}")
                    st.write("---")  # Add a separator for better readability
            else:
                st.write("No posts found with the tag 'yes'.")

    else:
        st.warning("Please enter both subreddits and keywords!")

# Input for sending messages
message = st.text_input("Enter your message", placeholder="Message")

# Button to send messages
if st.button("Send Message"):
    if message:
        st.success(f"Message sent: {message}")
    else:
        st.warning("Please enter a message to send!")
