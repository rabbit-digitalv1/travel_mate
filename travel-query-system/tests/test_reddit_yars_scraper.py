# tests/test_reddit_yars_scraper.py

import sys
import os

# Add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sources.reddit_yars_scraper import scrape_reddit
from scraper.preprocessor.cleaner import preprocess_post
from classifier.classify_post import classify_post_with_gemini

if __name__ == "__main__":
    subreddit = "Kathmandu"
    limit = 5

    print(f"🔍 Scraping r/{subreddit} (limit={limit})...")
    raw_posts = scrape_reddit(subreddit, sort="hot", limit = limit)

    processed_posts = []

    for post in raw_posts:
        print(f"\n🧼 Preprocessing: {post['title'][:60]}...")
        cleaned = preprocess_post(post)

        print("🤖 Classifying post with Gemini...")
        classification = classify_post_with_gemini(cleaned)

        cleaned["category"] = classification
        processed_posts.append(cleaned)

    print("\n✅ Final Processed + Classified Posts:")
    for p in processed_posts:
        print(f"👉 {p['title']} [{p.get('category', '❓')}]")
        if p.get("comments"):
            for i, comment in enumerate(p["comments"], 1):
                print(f"💬 {i}. {comment[:150]}{'...' if len(comment) > 150 else ''}")
        else:
            print("🚫 No comments found.")
        print("-" * 50)

