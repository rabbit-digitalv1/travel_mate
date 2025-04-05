# scraper/preprocessor/cleaner.py

import re
import unicodedata
from bs4 import BeautifulSoup


def strip_html(text):
    return BeautifulSoup(text, "html.parser").get_text()


def normalize_unicode(text):
    return unicodedata.normalize("NFKC", text)


def remove_urls(text):
    return re.sub(r"https?://\S+|www\.\S+", "", text)


def remove_special_chars(text):
    return re.sub(r"[^\w\s.,!?]", "", text)


def remove_extra_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_text(text: str) -> str:
    text = strip_html(text)
    text = normalize_unicode(text)
    text = remove_urls(text)
    text = remove_special_chars(text)
    text = remove_extra_whitespace(text)
    return text


def preprocess_post(post: dict) -> dict:
    cleaned_post = post.copy()
    cleaned_post["title"] = clean_text(post.get("title", ""))
    cleaned_post["body"] = clean_text(post.get("body", ""))

    if "comments" in post and isinstance(post["comments"], list):
        cleaned_post["comments"] = [clean_text(c) for c in post["comments"]]

    return cleaned_post
