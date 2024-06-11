import requests

HN_API_URL = "https://hacker-news.firebaseio.com/v0"


def get_top_stories():
    try:
        response = requests.get(f"{HN_API_URL}/topstories.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching top stories: {e}")
        return []


def get_story_details(story_id):
    try:
        response = requests.get(f"{HN_API_URL}/item/{story_id}.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching story details for {story_id}: {e}")
        return {}
