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


GROQ_API_KEY = "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"

client = Groq(
    api_key=GROQ_API_KEY,
)


def scrape(url_list):

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


    for url in urls:

    # Scraping the Jobs

        driver.get(url)
        time.sleep(1)
        print(f"Scraping {url}...")

        # Accept Reddit's cookies if prompted (optional)
        try:
            cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
            cookies_button.click()
        except:
            pass

        # # Scroll the page a few times to load more posts
        # scroll_pause_time = 2
        # scroll_count = 2

        # for _ in range(scroll_count):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(scroll_pause_time)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # After scrolling, get the page source for Beautiful Soup
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all post containers
        posts = soup.find_all(id=lambda x: x and x.startswith("post-title-t3_"))

        i=0
        # Loop through each post container and extract data
        
        for post in posts[:3]:
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

            post_data = {
                "Post ID": post_id,
                "UserID Link": user_id_link,
                "Title": title,
                "Flair": 'N/A Flair Text - Manually Added',
                "Description": description
            }
            scraped_data.append(post_data)
            i+=1

        for i in scraped_data:
            title = i['Title']
            if re.search(r'\[Hiring\]', title, re.IGNORECASE):
                i['Flair'] = "Job"
            elif re.search(r'\[Task\]', title, re.IGNORECASE):
                i['Flair'] = "Job"
            elif re.search(r'\[task\]', title, re.IGNORECASE):
                i['Flair'] = "Job"
            elif re.search(r'Task', title, re.IGNORECASE):
                i['Flair'] = "Job"
            elif re.search(r'Hiring', title, re.IGNORECASE):
                i['Flair'] = "Job"
            else:
                i['Flair'] = "Other"

        # Filter the scraped data to retain only entries with flair "Job"
        scraped_data = [job for job in scraped_data if job['Flair'] == "Job"]

    driver.quit()
    return scraped_data



def classify(scraped_data):
    # Flair and Tag Processing
    for i in scraped_data:
        # title = i['Title']
        # if re.search(r'\[For Hire\]', title, re.IGNORECASE):
        #     i['Flair'] = "For Hire"
        # elif re.search(r'\[Hiring\]', title, re.IGNORECASE):
        #     i['Flair'] = "Hiring"
        # elif re.search(r'\[Task\]', title, re.IGNORECASE):
        #     i['Flair'] = "Task"
        # else:
        #     i['Flair'] = "Other"

        # Define keyword patterns
        graphic_design_keywords = r"(photoshop|illustrator|UI/UX|graphic design|typography|posts)"
        # developer_keywords = r"(software development|programming|full-stack|backend|frontend|JavaScript|C\+\+|Java|Python|React|Angular|Node\.js|APIs|cloud computing|Git|RESTful|object-oriented programming|data structures|algorithms|Agile|CI/CD)"
        python_developer_keywords = r"(Python|Django|webscraper|webscrapper|webscrape|Flask|Pandas|NumPy|API development|REST APIs|FastAPI|object-oriented programming|data analysis|SQL|PostgreSQL|MySQL|MongoDB|machine learning|data science|ETL|testing|debugging|Git|unit testing|Docker|AWS|Azure|Lambda)"
        social_media_manager_keywords = r"(social media marketing|content creation|strategy|analytics|branding|Instagram|Facebook|Twitter|LinkedIn|TikTok|SEO|Hootsuite|Sprout Social|Buffer|Engagement|hashtags|campaigns|community management|metrics|advertising|paid ads|audience targeting)"
        video_editor_keywords = r"(video editing|Premiere Pro|After Effects|DaVinci Resolve|Final Cut Pro|motion graphics|color grading|visual effects|animation|storyboarding|YouTube|social media videos|audio editing|transitions|text overlays|video production|timelines|cutting|rendering|storytelling)"
        # mern_stack_developer_keywords = r"(MERN stack|MongoDB|Express\.js|React\.js|Node\.js|JavaScript|REST APIs|full-stack development|front-end|back-end|NoSQL|JWT authentication|React hooks|Redux|state management|MongoDB Atlas|Webpack|npm|Git|CSS|HTML|Agile)"

        description = i.get('Description', '')
        tags = "Other"

        if re.search(graphic_design_keywords, description, re.IGNORECASE):
            tags = "GD (graphic design)"
        if re.search(social_media_manager_keywords, description, re.IGNORECASE):
            tags = ("Social Media Manager")
        if re.search(video_editor_keywords, description, re.IGNORECASE):
            tags = ("Video Editor")
        if re.search(python_developer_keywords, description, re.IGNORECASE):
            tags = ("Python Developer")
        # if re.search(developer_keywords, description, re.IGNORECASE):
            # tags = ("Developer")
        # if re.search(mern_stack_developer_keywords, description, re.IGNORECASE):
            # tags = ("MERN Stack Developer")

        i['Tags'] = [tags]


    # # Print results with tags
    # for i in scraped_data:
    #     print(f"Title: {i['Title']}")
    #     print(f"Description: {i['Description'][:50]}")
    #     print(f"UserID Link: {i['UserID Link']}")
    #     print(f"Tags: {', '.join(i['Tags'])}")
    #     print("=" * 40)

    # print(f"Scraped for url : {url} \nTotal Scraped : {len(scraped_data)}") 
    
    return scraped_data




def classify_with_groq(desc):


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""Based on the description given below, respond with one word what the job is about. Choose one word from the following: Graphic Desginer , Video Editor , Python Dev

    """
            },
            {
                "role": "user",
                "content": f"Please respond to the following job description: \n{desc}"
            }
        ],
        model="llama3-8b-8192",
        max_tokens=1256,
    )



    print(chat_completion.choices[0].message.content)


    return True



def get_user_id(username):
    print("="*40)
    print("entered user id function")
    print("="*40)
    # Define the user's profile URL
    user_url = f"https://www.reddit.com/user/{username}/"
    user_url = username
    print(user_url)
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





def create_msg(description):

    portfolio_link = "https://zain2983.framer.website/"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""You are a skilled professional applying for a job via direct message. Your goal is to:

    - Craft a crisp, compelling application response
    - Highlight key qualifications matching the job description
    - Show genuine interest and professionalism
    - Keep the message concise (2-3 sentences max)

    Crucial Guidelines:
    1. Directly address the specific role
    2. Mention your most relevant experience
    3. If applicable, include a portfolio link
    4. Demonstrate why you're a great fit
    5. If necessary you are send  link for portfolio site {portfolio_link}



    Tone: Warm, confident, and professional"""
            },
            {
                "role": "user",
                "content": f"Job Description: {description}"
            }
        ],
        model="llama3-8b-8192",
        max_tokens=1256,
    )
    msg = (chat_completion.choices[0].message.content)
    return msg



if __name__ == "__main__":

    start_time = time.time()



    # url = "https://www.reddit.com/r/slavelabour/new/"
    # data1 = scrape(url_pram=url)
    # # data_w_tags = classify(scraped_data=data)

    # url = "https://www.reddit.com/r/forhire/new/"
    # data2 = scrape(url_pram=url)

    # # This data variable only contains Jobs 
    # # i.e only people looking to hire not people who are looking for job ( i.e no [For Hire] or [Offer] )
    # data = data1 + data2



    # url = "https://www.reddit.com/r/forhire/new/"
    # url = "https://www.reddit.com/r/slavelabour/new/"

    urls = [
        "https://www.reddit.com/r/forhire/new/",
        "https://www.reddit.com/r/slavelabour/new/",
    ]

    scraped_data = scrape(url_list=urls)
    # for i in data: 
    #     print(f"Title: {i['Title']}")
    #     print(f"Description: {i['Description'][:50]}")
    #     print(f"UserID Link: {i['UserID Link']}")
    #     print("=" * 40)
    
    
    data_w_tags = classify(scraped_data=scraped_data)

    print(type(data_w_tags))

    filtered_data = [entry for entry in data_w_tags if entry.get("Tags") == "Python Developer"]
    # filtered_data = data_w_tags

    for i in filtered_data:
        # print("UserID Link in for loop : " , i["UserID Link"])
        user_id = get_user_id(i["UserID Link"])  # Fetch user_id using the function
        i["user_id"] = user_id  # Add the fetched user_id to the dictionary


    for i in filtered_data:
        msg = create_msg(i["Description"])
        i['msg'] = msg


    # for i in filtered_data:
    #     print("="*40)
    #     print(i)




    #
    # Enter code here for sending messages
    #


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.4f} seconds")