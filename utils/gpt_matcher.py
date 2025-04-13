import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from config import USER_PROFILE

def create_prompt(job_description):
    return f"""
You are an AI that evaluates how well a job matches a user's profile.

User Profile:
- Title: {USER_PROFILE['title']}
- Summary: {USER_PROFILE['summary']}
- Experience: {', '.join(USER_PROFILE['experience'])}
- Education: {', '.join(USER_PROFILE['education'])}
- Project Highlights: {', '.join(USER_PROFILE['project highlights'])}
- Technical Skills: {', '.join(USER_PROFILE['technical skills'])}
- Professional Strengths: {', '.join(USER_PROFILE['professional strengths'])}
- Languages: {', '.join(USER_PROFILE['languages'])}
- Achievements: {', '.join(USER_PROFILE['achievements'])}

Job Description:
{job_description}

Score from 0 to 1 how well this job matches the user. Just return a float, no explanation.
"""

def get_match_score(job_description):
    prompt = create_prompt(job_description)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=10,
            temperature=0.2
        )

        score_text = response['choices'][0]['message']['content'].strip()
        score = float(score_text) * 100
        return round(score, 2)
    except Exception as e:
        print("Error getting match score:", e)
        return 0.0
    
def get_job_summary(description):
    prompt = f"Summarize the following job description in 1-2 sentences:\n\n{description}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize job descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        summary_text = response.choices[0].message.content.strip()
        return summary_text
    except Exception as e:
        print("Error getting job summary:", e)
        return None