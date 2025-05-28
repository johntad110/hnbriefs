import requests
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GENERATIVE_AI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash-001')

safety_config = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}


def summarize_story(url):
    try:
        story_content = fetch_article_content(url)
    except Exception as e:
        print(f"Error fetching article content from {url}: {e}")
        return "◕‿◕"

    try:
        soup = BeautifulSoup(story_content, 'html.parser')
        text = soup.get_text(separator='\n')

        response = model.generate_content(
            f"""
You are a professional summarizer with the storytelling ability of a world-class journalist and the brevity of a great copywriter and with the voice of a brilliant storyteller and the precision of a seasoned editor. Summarize the following Hacker News post in one short paragraph that’s short, punchy, engaging, captivating, human, and irresistible to read. Your job is to hook the reader and give them the essence without wasting a single word.

The summary must follow these rules:

- Be brief, sharp, and emotionally engaging  
- Tailor the tone to the topic (funny, serious, dramatic, curious — whatever fits)  
- Add a human touch. You’re not a robot—don’t sound like one  
- Use emojis naturally when they enhance the summary (not generic or filler)
- At the end, include relevant hashtags (no hyphens are allowed in hashtags)

If the provided article’s content is something could not be extracted or is clearly missing/blocked text, respond with:  
“Sorry, buddy. You gotta read this one on your own.”

Now, summarize this post like your reputation is on the line:

{text}

""",
            safety_settings=safety_config
        )
        return response.text
    except Exception as e:
        print(f"Error summarizing story from {url}: {e}")
        return "◕‿◕"


def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching article content from {url}: {e}")
        raise
