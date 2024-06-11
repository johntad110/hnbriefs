import requests
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GENERATIVE_AI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

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
            f"As a professional summarizer, summarize the following story in one paragraph! Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects. (At the end add a new line and then related Hash tags. NO hyphens (-) in the hashtags!)\n\n{text}", safety_settings=safety_config)
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
