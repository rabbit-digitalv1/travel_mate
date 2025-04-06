# scraper/sources/sessions.py
import random
import requests
from .agents import get_agent

class RandomUserAgentSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({"User-Agent": get_agent()})

    def request(self, *args, **kwargs):
        self.headers.update({"User-Agent": get_agent()})
        return super().request(*args, **kwargs)
