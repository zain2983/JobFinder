def main_func():
    import csv
    import re
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup
    import time

    # List of URLs to scrape
    urls = [
        "https://www.reddit.com/r/slavelabour/new/",
        # "https://www.reddit.com/r/forhire/new/",
        # "https://www.reddit.com/r/VideoEditor_forhire/new/",
        # "https://www.reddit.com/r/DoneDirtCheap/new/",
        # "https://www.reddit.com/r/freelance_forhire/new/",
    ]

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

    scraped_data = []

    for url in urls:
        driver.get(url)
        print(f"Scraping {url}...")

        # Accept Reddit's cookies if prompted (optional)
        try:
            cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
            cookies_button.click()
        except:
            pass

        # Scroll the page a few times to load more posts
        scroll_pause_time = 2
        scroll_count = 2

        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        # After scrolling, get the page source for Beautiful Soup
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all post containers
        posts = soup.find_all(id=lambda x: x and x.startswith("post-title-t3_"))

        # Loop through each post container and extract data
        for post in posts:
            post_id = post.get("id").replace("post-title-", "")
            title = post.get_text(strip=True)

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

    driver.quit()

    # Flair and Tag Processing
    for i in scraped_data:
        title = i['Title']
        if re.search(r'\[For Hire\]', title, re.IGNORECASE):
            i['Flair'] = "For Hire"
        elif re.search(r'\[Hiring\]', title, re.IGNORECASE):
            i['Flair'] = "Hiring"
        else:
            i['Flair'] = "Other"

        # Define keyword patterns
        graphic_design_keywords = r"(photoshop|illustrator|UI/UX|graphic design|typography|posts)"
        developer_keywords = r"(software development|programming|full-stack|backend|frontend|JavaScript|C\+\+|Java|Python|React|Angular|Node\.js|APIs|cloud computing|Git|RESTful|object-oriented programming|data structures|algorithms|Agile|CI/CD)"
        python_developer_keywords = r"(Python|Django|webscraper|webscrapper|webscrape|Flask|Pandas|NumPy|API development|REST APIs|FastAPI|object-oriented programming|data analysis|SQL|PostgreSQL|MySQL|MongoDB|machine learning|data science|ETL|testing|debugging|Git|unit testing|Docker|AWS|Azure|Lambda)"
        social_media_manager_keywords = r"(social media marketing|content creation|strategy|analytics|branding|Instagram|Facebook|Twitter|LinkedIn|TikTok|SEO|Hootsuite|Sprout Social|Buffer|Engagement|hashtags|campaigns|community management|metrics|advertising|paid ads|audience targeting)"
        video_editor_keywords = r"(video editing|Premiere Pro|After Effects|DaVinci Resolve|Final Cut Pro|motion graphics|color grading|visual effects|animation|storyboarding|YouTube|social media videos|audio editing|transitions|text overlays|video production|timelines|cutting|rendering|storytelling)"
        mern_stack_developer_keywords = r"(MERN stack|MongoDB|Express\.js|React\.js|Node\.js|JavaScript|REST APIs|full-stack development|front-end|back-end|NoSQL|JWT authentication|React hooks|Redux|state management|MongoDB Atlas|Webpack|npm|Git|CSS|HTML|Agile)"

        description = i.get('Description', '')
        tags = []

        if re.search(graphic_design_keywords, description, re.IGNORECASE):
            tags.append("GD (graphic design)")
        if re.search(developer_keywords, description, re.IGNORECASE):
            tags.append("Developer")
        if re.search(python_developer_keywords, description, re.IGNORECASE):
            tags.append("Python Developer")
        if re.search(social_media_manager_keywords, description, re.IGNORECASE):
            tags.append("Social Media Manager")
        if re.search(video_editor_keywords, description, re.IGNORECASE):
            tags.append("Video Editor")
        if re.search(mern_stack_developer_keywords, description, re.IGNORECASE):
            tags.append("MERN Stack Developer")

        i['Tags'] = tags if tags else ["Other"]

    # Print results with tags
    for i in scraped_data:
        print(f"Title: {i['Title']}")
        print(f"Description: {i['Description']}")
        print(f"Tags: {', '.join(i['Tags'])}")
        print("=" * 40)

if __name__ == "__main__":
    main_func()

