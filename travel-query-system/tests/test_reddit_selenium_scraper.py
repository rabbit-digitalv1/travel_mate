import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sources.reddit_scraper import scrape_reddit

# Call the function
posts = scrape_reddit("https://www.reddit.com/r/Kathmandu/", scroll_limit=3)

print("\n📝 Extracted Posts:\n")
for post in posts:
    print(f"• {post['title']}")
    print(f"  ↪ {post['url']}")
    print(f"  👤 {post['author']} | 👍 {post['upvotes']} | 💬 {post['comments']} | 🕒 {post['time_posted']}\n")
