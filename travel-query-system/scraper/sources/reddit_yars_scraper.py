from .utils.sessions import RandomUserAgentSession
import requests
import time
import random
import logging

logger = logging.basicConfig(
    filename="YARS.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class YARS:
    __slots__ = ("session", "proxy", "timeout")

    def __init__(self, proxy=None, timeout=10, random_user_agent=True):
        self.session = RandomUserAgentSession() if random_user_agent else requests.Session()
        self.proxy = proxy
        self.timeout = timeout

        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})

    def fetch_subreddit_posts(self, subreddit: str, limit=10, category="hot") -> list[dict]:
        base_url = f"https://old.reddit.com/r/{subreddit}/{category}.json"
        headers = {"User-Agent": self.session.headers.get("User-Agent")}
        params = {"limit": limit, "raw_json": 1}

        try:
            response = self.session.get(base_url, headers=headers, timeout=self.timeout, params=params)
            response.raise_for_status()
        except Exception as e:
            print("❌ Failed to fetch subreddit posts", e)
            return []

        posts = []
        data = response.json()
        for post in data.get("data", {}).get("children", []):
            d = post.get("data", {})
            posts.append({
                "title": d.get("title"),
                "author": d.get("author"),
                "permalink": d.get("permalink"),
                "score": d.get("score"),
                "num_comments": d.get("num_comments"),
                "created_utc": d.get("created_utc"),
            })
        return posts

    def scrape_post_details(self, permalink):
        url = f"https://www.reddit.com{permalink}.json"
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print("❌ Failed to fetch post details:", e)
            return []

        post_data = response.json()
        comments = []
        for item in post_data[1].get("data", {}).get("children", []):
            if item.get("kind") != "t1":
                continue
            comment_data = item.get("data", {})
            comments.append(comment_data.get("body", ""))
        return comments

def scrape_reddit(subreddit="Kathmandu", sort="hot", limit=5):
    yars = YARS()
    posts = yars.fetch_subreddit_posts(subreddit, limit=limit, category=sort)
    for post in posts:
        post["comments"] = yars.scrape_post_details(post.get("permalink"))
    return posts