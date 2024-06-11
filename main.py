import time
import datetime
import timeago
from apis.hn import get_top_stories, get_story_details
from apis.telegram import send_message
from summarizer import summarize_story
from cachetools import TTLCache

# Initialize an in-memory cache with a TTL of 3 days
cache = TTLCache(maxsize=1000, ttl=60 * 60 * 24 * 3)

SCORE_THRESHOLD = 150
FOUR_HOURS = datetime.timedelta(hours=4)
TWO_DAYS = datetime.timedelta(days=2)


def main():
    while True:
        start_time = time.time()
        try:
            top_stories = get_top_stories()  # Fetch top stories
            print(f"{len(top_stories)} top stories.")
        except Exception as e:
            print(f"Error fetching top stories: {e}")
            time.sleep(600)
            continue

        count = 0
        for story_id in top_stories:
            count += 1
            print(f"{count}. {story_id} | ", end="")
            # Check cache
            if story_id in cache:
                print(f"cached skipping. ")
                continue

            try:
                # Get story details
                story = get_story_details(story_id)
                print(
                    f"score {story.get('score')} | {story.get('title')} | ", end="")
                if story.get('score') < SCORE_THRESHOLD:
                    print("low score. ")
                    continue
            except Exception as e:
                print(f"Error getting story details for {story_id}: {e}")
                continue

            try:
                # Summarize story
                summary = summarize_story(story.get('url'))
                print('sumz-ed | ', end="")
            except Exception as e:
                print(f'Error summarizing story {story_id}: {e}')
                continue

            try:
                # Prepare message
                current_time = datetime.datetime.now()
                published_time = datetime.datetime.fromtimestamp(
                    story.get('time'))
                ago = timeago.format(current_time, published_time)
                status_emoji = ''
                delta = current_time - published_time
                if delta <= FOUR_HOURS:
                    status_emoji = '🔥 '
                elif delta >= TWO_DAYS:
                    status_emoji = '❄️ '
                message = f"<b>{story.get('title')}</b> ({status_emoji}Score: {story.get('score')}+ {ago})\n\n<b>Read more: </b><a href='{story.get('url')}'>{story.get('url')}</a>\n<b>Comments: </b><a href='https://news.ycombinator.com/item?id={story_id}'>https://news.ycombinator.com/item?id={story_id}</a> \n\n<b>Brief</b>: {summary}"

                buttons = []
                comments_count = story.get('descendants', 0)
                buttons.append({
                    'text': f"{comments_count}+ Comments",
                    'url':  f"https://news.ycombinator.com/item?id={story_id}"
                })

                buttons.append({
                    'text': 'Read',
                    'url': f"{story.get('url')}"
                })

                # Send message to Telegram
                send_message(message, reply_markup={
                             'inline_keyboard': [buttons]})
                print("sent.", end="")
            except Exception as e:
                print(
                    f"Error preparing/sending message for story {story_id}: {e}")
                continue

            # Cache the story ID
            cache[story_id] = True

        end_time = time.time()
        print("Finished one round in %s seconds. Sleeping for 10 min." %
              (end_time - start_time))

        # Sleep for 10 min
        time.sleep(600)


if __name__ == "__main__":
    main()
