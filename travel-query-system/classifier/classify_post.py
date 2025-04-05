# classifier/classify_post.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from scraper.preprocessor.cleaner import preprocess_post

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-pro")

FEW_SHOT_EXAMPLES = """
Example 1:
Title: "Looking for best coffee spots in Thamel"
Body: "Anyone knows a place that’s cozy with good cappuccino?"
Comments: ["Try Karma Coffee!", "Himalayan Java is classic."]
Category: Recommendation

Example 2:
Title: "Be careful with taxi scams!"
Body: "Charged double despite using meter. Near the airport."
Comments: ["Same happened to me", "Use Pathao or Tootle next time."]
Category: Warning

Example 3:
Title: "German Speakers based in Kathmandu?"
Body: "Looking to connect with German travelers or expats."
Comments: ["You’ll find some around Thamel", "Try Couchsurfing groups"]
Category: General Query

Example 4:
Title: "Trip to Nagarkot was magical"
Body: "Sunrise from the hills was a life experience."
Comments: ["Loved it there", "I agree!"]
Category: Experience

"""

# Simple keyword-based fallback rule
KEYWORD_RULES = {
    "recommend": "Recommendation",
    "suggest": "Recommendation",
    "where": "General Query",
    "anyone": "General Query",
    "help": "General Query",
    "warning": "Warning",
    "scam": "Warning",
    "bad": "Warning",
    "terrible": "Warning",
    "i ": "Experience",
    "my ": "Experience",
}

def rule_based_classification(post):
    title = post.get("title", "").lower()
    body = post.get("body", "").lower()
    for keyword, category in KEYWORD_RULES.items():
        if keyword in title or keyword in body:
            return category
    return None

def classify_post_with_gemini(post: dict) -> str:
    fallback = rule_based_classification(post)
    if fallback:
        return fallback

    p = preprocess_post(post)
    content = f"""
{FEW_SHOT_EXAMPLES}
Now classify this:

Title: {p['title']}
Body: {p['body']}
Comments: {' | '.join(p['comments'][:3])}

Return ONLY the category name from:
- Recommendation
- Experience
- General Query
- Warning
- Other
"""
    try:
        response = model.generate_content(content)
        return response.text.strip()
    except Exception as e:
        print("Gemini Classification Error:", e)
        return "Other"

# Example usage
if __name__ == "__main__":
    sample_post = {
        "title": "Where can I find good momo in Thamel?",
        "body": "I'm traveling to Kathmandu and would love some recommendations for local momo spots.",
        "comments": ["Try Momo Hut", "OR2K is decent", "Go to Yangling"]
    }
    print("🧠 Classification Result:", classify_post_with_gemini(sample_post))
