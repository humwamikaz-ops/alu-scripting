#!/usr/bin/python3
"""Query the Reddit API for the number of subscribers of a subreddit."""
import requests


def number_of_subscribers(subreddit):
    """Return the total number of subscribers of a subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: The number of subscribers, or 0 if the subreddit is invalid.
    """
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:api_advanced:v1.0"}

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return 0

    try:
        return response.json().get("data", {}).get("subscribers", 0)
    except ValueError:
        return 0
