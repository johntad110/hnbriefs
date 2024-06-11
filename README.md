# Hacker News Briefs Bot

A Telegram bot that posts new hot stories from Hacker News to the [Hacker News Briefs Telegram channel](https://t.me/hnbriefs), including a short summary of each story.

## Overview

The Hacker News Briefs Bot fetches top stories from Hacker News every 10 minutes and posts those that have reached a score of 100 or more to a [Telegram channel](https://t.me/hnbriefs), along with a brief summary.

## Features

- Fetches top stories from Hacker News using the [Hacker News API](https://github.com/HackerNews/API).
- Summarizes each story using a language model.
- Posts the title, score, summary, and links to the article and comments to a Telegram channel using the [Telegram Bot API](https://core.telegram.org/bots/api).

## Requirements

- Python 3.x
- A Telegram bot token (register via [BotFather](https://t.me/BotFather))
- An API key for a language model (e.g., OpenAI's GPT-4, or Google's Gemini)

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/johntad110/hnbriefs.git
   cd hnbriefs
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the project root and add your API keys:

   ```
   OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
   TG_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
   TG_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
   ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

## Usage

Once the bot is running, it will automatically fetch top stories from Hacker News every 10 minutes, summarize them, and post to the configured Telegram channel.

## File Structure

- `main.py`: Coordinates the entire process, including fetching stories, summarizing, and posting to Telegram.
- `hn.py`: Contains functions to interact with the Hacker News API.
- `telegram.py`: Contains functions to interact with the Telegram Bot API.
- `summarizer.py`: Contains functions to summarize articles using a language model API.

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
