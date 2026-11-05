#!/usr/bin/python3
"""Recursively count keywords in the titles of hot posts of a subreddit."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found in hot post titles.

    Matching is case-insensitive and whole-word only, so "java." does not
    count as "java". Duplicate keywords in word_list add their counts
    together. Prints nothing if there are no matches or the subreddit is
    invalid.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): The keywords to count.
        after (str): Pagination token for the next page (used by the
            recursion).
        counts (dict): Occurrences found so far (used by the recursion).
    """
    if counts is None:
        counts = {}

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:api_advanced:v1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return

    try:
        data = response.json().get("data", {})
    except ValueError:
        return

    keywords = [word.lower() for word in word_list]
    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for word in title.lower().split():
            if word in keywords:
                counts[word] = counts.get(word, 0) + 1

    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, counts)

    results = {}
    for word, number in counts.items():
        results[word] = number * keywords.count(word)

    for word, number in sorted(results.items(),
                               key=lambda item: (-item[1], item[0])):
        print("{}: {}".format(word, number))
