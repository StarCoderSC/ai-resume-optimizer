AI Resume vs Job Description Analyzer

An AI-powered web application built with Python, Streamlit, and OpenAI API that compares resumes against job descriptions and provides structured, recruiter-style feedback.

Live App: https://smart-resume-ai.streamlit.app/

🚀 Features

📊 Resume vs JD match score (weighted skill analysis)

🔎 Missing skill detection

🧠 Structured AI recruiter-style feedback

✍️ Bullet point rewriting with OpenAI

📄 PDF and TXT support

⏱ Session-based AI usage limits

🔒 API rate limit protection (cooldown logic)

🔑 Premium access code system (beta version)


🧠 How It Works

1. Upload resume and job description (PDF or TXT)

2. Text is extracted and normalized

3. Skills and phrases are matched with weighted scoring

4. OpenAI generates structured feedback

5. Session limits and cooldown protect API usage



🛠 Tech Stack

Python

Streamlit

OpenAI API

pdfplumber

Git & GitHub


📦 Installation (Local Setup)

Clone the repository:

``` Bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

# Install dependencies:

streamlit run app.py

# Run the app:

streamlit run app.py