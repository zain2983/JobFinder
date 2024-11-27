import os

from groq import Groq


GROQ_API_KEY = "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"

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
            "content": f"""You are applying for a job in an infromal way. A description has been posted and your task is to respond directly and concisely. Keep your response within 1-2 lines. Be direct and to the point.

            If the job is regarding video editing or graphic design, include this link in your response: {portfolio_link}.
            
            Here are some examples of how to respond:
            1. 'Hi, I want to apply for the Graphic Designer Position. I have almost 5 years of experience working as a graphic deisgner and social media manager. This is the link to my portfolio : {portfolio_link} Kindly take a look and please let me know if you have any questions.'
            2. 'I want to apply for the Video editor position. I have almost 5 years of experience. Kindly take a look at my portfolio : {portfolio_link}.'
            3. 'I have a proven track record in delivering creative designs tailored to client needs. My portfolio: {portfolio_link}.'
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