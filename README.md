
# JobFinder  
A Reddit-job-scraping + Google Sheets automation tool

## 🚀 Overview  
**JobFinder** is a Python automation tool that scrapes job posts from the Reddit subreddit **r/forhire**, filters them based on your criteria, and saves relevant posts directly into a Google Sheet.  
It's perfect for freelancers, agencies, or anyone who wants to monitor new job opportunities in real-time without manually checking Reddit.

---

## ✅ Features  
- Scrapes new posts from **r/forhire**  
- Evaluates each post for relevance using predefined rules  
- Automatically logs matching posts into a Google Sheet  
- Prevents duplicates by checking existing entries  
- Easy to modify, customize, and expand  

---

## 📁 Project Structure  
```

JobFinder/
│
├── main.ipynb        # Main scraping logic
├── sheets.ipynb      # Google Sheets integration
├── modules/          # Helper scripts and configurations
├── trial/            # Experimental or test notebooks
└── .gitignore

````

---

## 🛠 Requirements  
Before running the project, install:

```bash
pip install gspread google-auth selenium webdriver-manager
````

You also need:

* A Google Cloud project with **Google Sheets API** enabled
* OAuth credentials (`client_id`, `client_secret`, etc.)
* A target Google Sheet to store the scraped job posts
* ChromeDriver (or rely on `webdriver-manager`)

---

## 🔧 Setup

### 1. Google Sheets

* Enable Google Sheets API
* Download your OAuth credentials JSON
* Place it in the project directory
* Share your target Google Sheet with the service account email

### 2. Configuration

Inside the `modules/` folder or config section:

* Add your Google Sheets credentials
* Set your target sheet name/ID
* Define your filtering rules (keywords, budget, skill-match, etc.)

---

## ▶️ How to Run

### **Step 1:** Scrape Reddit

Open and run all cells in:

```
main.ipynb
```

This collects new posts from r/forhire and stores them locally.

### **Step 2:** Push to Google Sheets

Open and run:

```
sheets.ipynb
```

This sends filtered results into your Google Sheet while avoiding duplicates.

---

## 🧠 Suggested Improvements

* Convert notebooks into Python scripts or a CLI tool
* Add multi-subreddit support
* Trigger periodic scraping via cron or GitHub Actions
* Replace Google Sheets with PostgreSQL or Firebase
* Add NLP-based post scoring
* Build a small dashboard (Next.js + Tailwind)
* Send email or WhatsApp alerts for high-value job posts

---

## 👤 Contributor

[Muhammad Hamza Ahmad](https://github.com/HamzaAhmad6292)



