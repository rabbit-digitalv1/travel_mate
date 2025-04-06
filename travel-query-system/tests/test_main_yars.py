import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sources.yars import YARS
from scraper.sources.utils.utils import export_to_json

yars = YARS()

result = yars.scrape_full_posts(subreddit="NepalSocial", limit=5)

export_to_json(result, "reddit_posts.json")


# print(f"Results: {str(result)}")
