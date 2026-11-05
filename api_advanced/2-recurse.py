#!/usr/bin/python3
"""Recursively collect the titles of all hot posts of a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of titles of all hot posts of a subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): Titles collected so far (used by the recursion).
        after (str): Pagination token for the next page (used by the
            recursion).

    Returns:
        list: The titles of all hot posts, or None if there are no
            results or the subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:api_advanced:v1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return hot_list or None

    try:
        data = response.json().get("data", {})
    except ValueError:
        return hot_list or None

    for post in data.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))

    after = data.get("after")
    if after is None:
        return hot_list or None

    return recurse(subreddit, hot_list, after)
