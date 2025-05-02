import os

from groq import Groq


GROQ_API_KEY = ""

client = Groq(
    api_key=GROQ_API_KEY,
)


gd_portfolio = "https://www.behance.net/zenith_studio"
python_dev_portfolio = "https://zain2983.framer.website/"
portfolio_link = "XXXXXXXX"


desc = """
Description: [HIRING] Fashion Branding Designer for Luxury Logo - Budget $150 & UP
I’m seeking a designer with experience in fashion branding to create a minimalist, high-end logo for my luxury brand. The logo should convey elegance, exclusivity, and a timeless style that aligns with luxury fashion. And this is also an opportunity for new graduates looking to build their portfolio Please before dm meet
Requirements: •	Experience in designing for fashion or luxury brands •	Strong portfolio showcasing clean, sophisticated branding work
Budget: $150 & Up
To Apply: Please DM with: 1.	A link to your portfolio, especially any work with luxury or fashion brands. 2.	Confirmation that the budget is workable. 3.	Any initial questions about the project.
Thank you!
Tags: Video Editor, Graphic

"""

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
            "content": f"Job Description: {desc}"
        }
    ],
    model="llama3-8b-8192",
    max_tokens=1256,
)



print(chat_completion.choices[0].message.content)