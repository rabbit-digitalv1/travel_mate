import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sources.reddit_yars_scraper import scrape_reddit
from scraper.preprocessor.cleaner import preprocess_post

print("🔄 Scraping + Preprocessing /r/Kathmandu (limit=3)")
raw_posts = scrape_reddit("Kathmandu", sort="hot", limit=3)

print(f"✅ Raw posts fetched: {len(raw_posts)}\n")
print("🧹 Cleaned Posts:\n")

for i, post in enumerate(raw_posts, 1):
    cleaned = preprocess_post(post)
    print(f"📌 Post {i}:")
    print(f"🧾 Title: {cleaned['title']}")
    print(f"💬 Comments:")
    if cleaned["comments"]:
        for j, c in enumerate(cleaned["comments"], 1):
            print(f"   {j}. {c}")
    else:
        print("   ❌ No comments.")
    print()
