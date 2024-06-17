import re


def extract_hn_ids(text):
    """Extract Hacker News item IDs from the given text."""
    hn_url_pattern = re.compile(r'https://news.ycombinator.com/item\?id=(\d+)')
    return hn_url_pattern.findall(text)
