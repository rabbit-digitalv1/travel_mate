# scraper/sources/sessions.py
import random
import requests
from yarl import URL

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    # Add more real-world user agents or rotate with faker
]

class RandomUserAgentSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({"User-Agent": random.choice(USER_AGENTS)})

    def request(self, *args, **kwargs):
        self.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        return super().request(*args, **kwargs)
