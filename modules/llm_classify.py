import os

from groq import Groq


GROQ_API_KEY = ""

client = Groq(
    api_key=GROQ_API_KEY,
)


portfolio_link = "https://www.behance.net/zenith_studio"

desc = """
Description: [HIRING] Fashion Branding Designer for Luxury Logo - Budget $150 & UP
I’m seeking a designer with experience in fashion branding to create a minimalist, high-end logo for my luxury brand. The logo should convey elegance, exclusivity, and a timeless style that aligns with luxury fashion. And this is also an opportunity for new graduates looking to build their portfolio Please before dm meet
Requirements: •	Experience in designing for fashion or luxury brands •	Strong portfolio showcasing clean, sophisticated branding work
Budget: $150 & Up
To Apply: Please DM with: 1.	A link to your portfolio, especially any work with luxury or fashion brands. 2.	Confirmation that the budget is workable. 3.	Any initial questions about the project.
Thank you!
Tags: Video Editor, Graphic Desgin

"""

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